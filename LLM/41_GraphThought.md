# **GraphThought: Graph Combinatorial Optimization with Thought Generation** 

**Zixiao Huang**<sup>**1**</sup> **, Lifeng Guo**<sup>**1,5**</sup> **, Wenhao Li**<sup>**2**</sup> **, Junjie Sheng**<sup>**3**</sup> **, Chuyun Shen**<sup>**1**</sup> **, Haosheng Chen**<sup>**1**</sup> , **Xiangfeng Wang**<sup>**1,5**</sup> , **Changhong Lu**<sup>**1,5**</sup> , **Bo Jin**<sup>**2,4***</sup> 

1East China Normal University 2Tongji University 3Independent Researcher 4Shanghai Research Institute for Intelligent Autonomous Systems, Tongji University 5Key Laboratory of Mathematics and Engineering Applications, MoE, East China Normal University 

## **Abstract** 

Graph combinatorial optimization (GCO) problems are central to domains like logistics and bioinformatics. While traditional solvers dominate, large language models (LLMs) offer new possibilities for structured reasoning, yet struggle with complex GCO tasks requiring rigorous combinatorial analysis and multi-step deduction, often producing hallucinated steps. We first formalize the _Optimal Thoughts Design_ (OTD) problem, which provides a structured guidance for producing high-quality intermediate reasoning steps. Building on this formulation, we introduce _GraphThought_ , a novel framework that generates effective reasoning sequences through either heuristic-guided _forward_ search or solver-aligned _backward_ reasoning. By fine-tuning LLMs on these structured thought sequences<sup>1</sup> , we develop Llama-GT, an 8B-parameter model that achieves state-of-theart performance on the GraphArena benchmark, outperforming significantly larger models like DeepSeek-V3. Our results demonstrate that when scaffolded with structured reasoning priors, principled thought generation can significantly enhance LLM performance on GCO tasks without requiring increased model scale. 

## **1 Introduction** 

Graph combinatorial optimization (GCO)problems constitute a broad class of computationally challenging tasks defined over graph structures, ranging from shortest-path and optimal tour routing to selecting maximum independent sets (MIS) or minimum vertex covers (MVC). These problems, which have driven fundamental advances in discrete mathematics and computer science for decades (Kuhn, 1955; Kruskal, 1956; Jr. and Fulkerson, 1956), 

> *Emails: {zxhuang, cyshen, 51265901016, jarvis}@stu.ecnu.edu.cn; {lfguo, chlu}@math.ecnu.edu.cn; {whli, bjin}@tongji.edu.cn; xfwang@sei.ecnu.edu.cn 

> 1Dataset is available at https://anonymous.4open. science/r/GraphThought-7CFE. 

manifest across diverse application domains including logistics optimization, electronic circuit design, bioinformatics, and social network analysis (Tang et al., 2025). Many canonical GCO tasks—most notably the traveling salesman problem (TSP) and MIS—remain NP-hard, motivating ongoing research into both exact and approximation techniques. 

Traditional approaches to GCO have predominantly relied on human-designed algorithms and heuristics. Over decades, researchers have developed various methodologies including greedy algorithms, local search techniques, branch-and-bound approaches, and approximation schemes, which demonstrate notable effectiveness on moderatescale instances (Kuhn, 1955; Jr. and Fulkerson, 1956; Kruskal, 1956; Paschos, 2014). While such manually engineered approaches often produce satisfactory solutions, they require substantial manual effort and domain-specific expertise. Furthermore, heuristics constrained by fixed patterns (e.g., selecting minimum-degree nodes in MIS) often fail to account for global optimality, potentially leading to suboptimal outcomes through locally optimal choices, which can be observed in Figure 1. 

In recent years, deep neural network–based approaches have attracted considerable attention for addressing GCO problems by learning solutions in a data-driven manner. Methods based on deep reinforcement learning and graph neural networks have demonstrated the ability to learn heuristics for specific tasks like TSP and MIS, often treating the problem solver as a black-box model optimized end-to-end (Jin et al., 2024b; Jiang et al., 2024b; Liu et al., 2023c; Iklassov et al., 2024; Lehnert et al., 2024b). However, a major drawback is that each problem typically requires a specialized network architecture or input encoding – for instance, a model architecture tailored for routing problems may not directly work for MIS, necessitating bespoke representation engineering per task (Jiang 

1 



<!-- Start of picture text -->
“Aha Moment”<br>Greedy ......<br>Llama-GT ......<br>1 2 3 ...... 12 ...... Final Solution<br>Step<br><!-- End of picture text -->

Figure 1: Comparative Analysis of Greedy Algorithm versus LLM-Generated Solution for MIS. Upper: Stepwise greedy selection process (e.g., selecting node 16, then removing neighbors 21 and 17), yielding an **11** - node solution. Lower: Llama-GT-generated solution employing adaptive heuristics (e.g., prioritizing node 18 and removing neighbors 2, 15, 23), achieving a superior **12** -node independent set. _Color legend:_ yellow = isolated nodes; green = selected nodes; red = neighbors of current selection; gray = removed nodes. 

et al., 2024b; Jin et al., 2024b). Moreover, pure learning-based solvers often fail to exploit obvious problem-specific priors that humans would incorporate. 

Recent work has explored using LLMs for GCO through natural language reasoning, where models process graph descriptions and generate stepwise solutions by leveraging embedded algorithmic knowledge (Wang et al., 2022; Ren et al., 2024b; Li et al., 2024a; Liu et al., 2023b; Luo et al., 2024a). This paradigm offers flexibility across problems through textual problem phrasing and recall of training-exposed strategies (Li et al., 2024a; Ren et al., 2024b), achieving promising zero-shot/fewshot performance on small-scale tasks (Wang et al., 2022; Liu et al., 2023b). However, LLMs significantly trail dedicated solvers on NP-hard problems like MIS and graph coloring, with benchmarks revealing poor solution optimality and validity even for advanced models like GPT-4 (Tang et al., 2025; Wang et al., 2022). Critical challenges include hallucinated reasoning steps (Liu et al., 2023b; Luo et al., 2024a) and unreliable multi-step deduction, despite mitigation attempts through structured prompts (Luo et al., 2024a; Ouyang et al., 2024a; Skianis et al., 2024a; Sanford et al., 2024b; Li et al., 2024b). While various approaches employ prompt engineering, code generation, or non-text embeddings (Jin et al., 2024a; Chen et al., 2024b; Liu et al., 2023a; Ren et al., 2024a), their perfor- 

mance remains substantially inferior to commercial solvers like Gurobi, highlighting limitations in directly mapping problems to solutions without addressing GCO’s inherent long-horizon reasoning requirements. This raises an intuitive question: _Can we incorporate the search principles of classical GCO solvers into the LLM’s output process?_ 

Related ideas have been proposed to enhance the general problem-solving capabilities of LLMs, such as simulating human cognitive processes by generating intermediate thoughts prior to final responses. Methods like chain- (Wei et al., 2022), tree- (Yao et al., 2024) and graph-ofthoughts (Besta et al., 2024a) prompting encourage step-by-step reasoning (Besta et al., 2024b). While these techniques are often effective, they can sometimes degrade performance due to selfenforcing (Huang et al., 2024). Moreover, techniques that work well on one dataset may not generalize to others due to variations in the type of reasoning involved (e.g., spatial reasoning vs. mathematical reasoning) (Lehnert et al., 2024a; Wu et al., 2024). Similar limitations appear in recent GCO-focused works (Luo et al., 2024b; Lehnert et al., 2024a; Chen et al., 2024a; Zhang et al., 2024; Ouyang et al., 2024b; Gandhi et al., 2024), which construct thoughts by unrolling search algorithms or generating them via LLMs, followed by supervised fine-tuning. However, thought generation in GCO presents a unique challenge: _For NP-hard or NP-complete problems, no efficient traditional (heuristic) search methods exist, rendering forward thought construction infeasible._ 

To address this, the Optimal Thoughts Design (OTD) problem is formally defined through a unified thought representation framework that systematically encodes search principles into LLM reasoning processes. The OTD formulation introduces action thought spaces A and state thought spaces S to model reasoning trajectories, enabling the generation of high-quality solution paths for GCO tasks. Building on this foundation, GraphThought—a novel framework that consists of forward and backward thought generation paradigms—is proposed. The forward mode employs heuristic-guided mechanisms for tractable problems, while the backward mode implements solver-guided backtracking techniques to handle NP-hard challenges. 

Through extensive experiments, Llama-GT is developed by fine-tuning the Llama-3-8B-Instruct model using reasoning data generated by the proposed framework. Comprehensive evaluations 

2 



<!-- Start of picture text -->
0 1 s6 Describe neighbor nodesof the chosen node s1 Whether the end nodehas been found<br>2 3 a2 Add nodes based on BFS s8 Desribe the current pathfound so far s9 Describe the shortestpath<br>shortest path<br>Selector Constructor<br>Forward Polynomial- Extract Forward<br>GCO Task time Task Heuristic Synthesis Program<br>MIS<br>MVC Design  Design Dataset<br>TSP Action State Generation<br>...<br>Synthesis Backward<br>NP-Hard Task AddOne with<br>Backward Solver Program<br>0 1 a1 Add nodes based on thegiven optimal solution s1 Whether there are anynodes left in the graph s8 Describe current solution set<br>2 4 3 a3 Add isolated nodes s6 Describe neighbor nodesof chosen nodes s6 Describe the remaining nodesin the graph<br>Independent SetMaximum s3 Remove neighbor nodes ofchosen nodes from the graph s9 Describe final solution set<br><!-- End of picture text -->

Figure 2: The _Forward_ and _Backward_ MTP frameworks for constructing the **Selector** and **Constructor** modules in GraphThought through distinct pathways. The **Selector** extracts action-state pairs from spaces A and S, while the **Constructor** synthesizes an executable program. Two paradigm examples are shown: (1) Forward MTP for polynomial problems (e.g., shortest path) uses heuristic extraction of action thoughts (e.g., BFS-based node addition) to guide state selection; (2) Backward MTP for NP-hard problems (e.g., MIS) reconstructs reasoning steps through solver-derived solutions and reverse analysis. Both frameworks generate programs via systematic composition of thought sets, with backward MTP requiring combinatorial solvers. Appendix L shows detailed reasoning steps, with full thought spaces described in Appendix G. 

across diverse GCO tasks demonstrate remarkable performance improvements, encompassing both polynomial-time solvable and NP-hard problems. Testing was conducted on graphs varying from small-scale (few nodes) to medium-scale (dozens of nodes). Llama-GT achieves solution quality that approaches the optimality bounds of commercial solvers like Gurobi in certain tasks, while retaining the flexibility of LLM-based reasoning. 

The main contributions are as follows: 1) We formalize the OTD problem with state thought space S and action thought space A, which facilitates the systematic generation of reasoning thoughts. 2) Within the GraphThought framework, we propose dual thought generation frameworks: a forward (heuristic-guided) one and a backward (solverguided) one for GCO problems. 3) The state-ofthe-art performance of our approach is evidenced by the fine-tuning of Llama-3-8B-Instruct, which achieves superior accuracy on GraphArena, outperforming both proprietary and open-source LLMs by significant margins. and approaching the performance of the commercial solver Gurobi. 

## **2 Problem Formulation** 

This section formalizes the core problems addressed in this work. Despite the rapid progress of large language models (LLMs) across scientific and engineering domains, a key challenge remains in adapting them to complex mathematical tasks requiring advanced reasoning and domain-specific knowledge. 

Combinatorial optimization (CO) problems form a class of mathematical optimization problems where the objective is to identify the optimal solution from a finite or countably infinite set of discrete candidates. Solving CO problems typically requires carefully crafted heuristic algorithms, often derived through rigorous mathematical analysis. These algorithms integrate sophisticated strategies to balance solution quality and computational efficiency. These algorithms embody sophisticated strategies to balance solution quality and computational efficiency. A fundamental challenge lies in incorporating the search principles of heuristic algorithms into learnable reasoning thoughts for LLMs, enabling knowledge transfer while preserving algorithmic efficiency. We focus on GCO problems because graphs naturally model a variety of CO problems. A graph rep- 

3 

resents discrete entities through nodes and their connections. For a graph _G_ = ( _V, E_ ), the node set _V_ = _{v_ 1 _, . . . , vn}_ contains _n_ nodes, while the edge set _E_ = _{e_ 1 _, . . . , em}_ defines _m_ adjacency relationships. An edge _e_ = ( _vi, vj_ ) denotes the adjacency of nodes _vi_ and _vj_ . Formally, let _F_ : (LLM _, D_ ) _→_ LLM _D_ denote the supervised fine-tuning process mapping a foundation LLM to its fine-tuned version LLM _D_ through the training dataset _D_ . The evaluation metric _M_ : LLM _D →_ R<sup>+</sup> measures model performance. The core optimization challenge is formalized as: 



where _D_<sup>_∗_</sup> is the optimal training dataset given LLM, _F_ , and _M_ . The formulation (1) constitutes a CO challenge over the exponentially large space of possible training datasets _D_ . Three key difficulties emerge: 1) The discrete solution space prohibits gradient-based optimization; 2) The black-box nature of _M_ prevents analytical evaluation; 3) The computational cost of evaluating _M_ grows superlinearly with instance size. It becomes important to efficiently compute high-quality approximate optimal solutions of (1). 

Thoughts of solving specific instances of math problems can be viewed as high-quality training data for fine-tuning LLMs and thus developing enhanced thoughts is critical for the creation of superior training datasets. In the following, we will propose a series of thought generation methods to establish thoughts as one kind of approximate suboptimal solutions for the formulation (1). 

The representation and design of thoughts are typically a promising research direction in order to enhance the reasoning capabilities of LLMs. The thought generation process can be modeled as to solve an approximate optimal solution _D_<sup>_′_</sup> _⊂ D_<sup>ˆ</sup> for the formulation (1), where _D_<sup>ˆ</sup> denotes the set of all training data with thoughts as content. For GCO problems, there are mainly two kinds of thoughts. One kind is to decide the following available action executed on the instance and the other kind is to show the current solving state. A hierarchical decision problem in generating these kinds of thoughts is govern as: 



where A and S denote the action thought space and state thought space for a GCO problem, respectively. The first item is to choose optimal _A_<sup>_∗_</sup> from 

A and optimal _S_<sup>_∗_</sup> from S according to the characteristics of the GCO problem, where _A_ encapsulates core algorithmic operations while _S_ maintains dynamic problem-solving states. The second item is to incorporate all chosen thoughts of _A_<sup>_∗_</sup> and _S_<sup>_∗_</sup> into a program template _P_ , which is used to generate specific thoughts in solving a GCO instance. 

In summary, the OTD problem is to generate the optimal thought set _A_<sup>_∗_</sup> and _S_<sup>_∗_</sup> to construct a program _P_ for a GCO problem, which is the key problem to be addressed in this work. To emphasize, the optimal thoughts dataset in OTD might not be the optimal solution of the formulation (1), but it can be considered as a high-quality approximate solution. 

## **3 The GraphThought Framework** 

### **3.1 The Overall Framework** 

GraphThought is introduced as a novel framework for fine-tuning LLMs through reasoning thought generation, as formalized in Algorithm 1. The architecture of the framework comprises two core modules that collaboratively generate task-specific reasoning programs by selecting state and action thoughts and constructing programs, denoted as **Selector** and **Constructor** , respectively. 

- **Selector** : For a given task _τ_ , this module performs dynamic selection of _action-state pairs_ ( _A, S_ ) from predefined action and state thought space A and S. The selection mechanism adaptively adjusts its strategies to capture the essential characteristics of _τ_ , ensuring context-aware component selection; 

- **Constructor** : This module operates as a program synthesis engine that methodically assembles the selected ( _A, S_ ) into an executable program _P_ . 

For the predefined action thought space A and state thought space S, we systematically derive nine state representations and sixteen action operators through rigorous analysis of task-solving processes. These elements constitute the fundamental components of our framework, where A primarily represents operations on the solution set (e.g., adding nodes or edges), while S captures both graph operations (e.g., node insertion/removal) and state descriptions (e.g., remaining nodes/edges, current solution status). Complete specifications are provided in Appendix G. 

The synthesized program _P_ serves dual objectives: 1) as an algorithmic solver for task _τ_ , and 2) as a structured data generator for creating reasoning thoughts. Through iterative execution on instances 

4 

set _D_<sup>˜</sup> _τ_ , where _|D_<sup>˜</sup> _τ |_ = _n_ , _P_ produces structured reasoning thoughts set _T_ = _{Ti}_<sup>_n_</sup> _i_ =1<sup>that form the</sup> training corpus for LLM fine-tuning. 

**Algorithm 1** Thought-Enhanced LLM Fine-Tuning 

- **Require:** S, foundation modelTarget task _τ_ , problem instancesLLM;˜ _D_<sup>˜</sup> _τ_ , A, 

- 1: ( _A, S_ ) _←_ **Selector** ( _τ,_ A _,_ S); _▷_ Action/State set selection 

- 2: _P ←_ **Constructor** ( _τ, A, S_ ); _▷_ Program synthesis 

- 3: Initialize thought corpus _T ←∅_ ; 

- 4: **for** _i_ = 1 to _|D_<sup>˜</sup> _τ |_ **do** 5: Select an instance _Ii ← D_<sup>˜</sup> _τ_ [ _i_ ]; 

- 6: Generate thought _Ti ←P_ ( _Ii_ ); _▷_ Program execution 

- 7: _T ← T ∪{Ti}_ ; 8: **end for** 9: **return** LLMfine-tuned _←F_ (LLM˜ _, T_ ). 

To achieve the functionalities of **Selector** and **Constructor** , we propose **Meta-Thought Programming (MTP)** , a systematic methodology for generating ( _A, S, P_ ) triples through structured knowledge extraction. For GCO problems, we develop two MTP frameworks as follows: 

- **Forward MTP** : decomposes classical heuristic algorithms to extract fundamental reasoning patterns through constructive forward-chaining; 

- **Backward MTP** : discovers implicit reasoning principles via backward analysis of high-quality solutions. 

The GraphThought framework, designed to address the OTD problem, embodies the dual-process framework depicted in Figure 2. The proposed framework consists of two independent components: the forward framework illustrated in the upper half of the figure, whereas the backward one is correspondingly demonstrated in the lower half. The architectural components will be discussed in the following two subsections, collectively establishing the OTD solution set. 

### **3.2 Forward MTP Framework** 

The green-highlighted modules in Figure 2 formally establish the forward MTP framework. For a given GCO task _τ_ , this framework systematically extracts several classical heuristic algorithms. These algorithms are systematically combined to distill fundamental operations from A, thereby constructing the action thought set _A_ . Concurrently, 

the corresponding state thought set _S_ is axiomatically derived from S with _A_ and _τ_ . Following this procedural logic, the target program _P_ is synthesized via categorical composition of selected _A_ - _S_ pairs. The complete generation mechanisms of _A_ and _S_ is rigorously detailed in Appendix F. 

A basic program template of _P_ is structured in Program Template 1. It sequentially applies action thoughts in _A_ followed by displaying each state of _S_ . This template may require domainspecific adaptations depending on the task _τ_ . An application of the forward MTP framework for the connected components problem is introduced in Appendix H.1. 

**Program 1** A Forward MTP Program Template 

- **Require:** Instance _I_ , state and action thought set _S, A_ . 

- 1: Initialize an empty solution _x ←∅_ 

- 2: Initialize a solving flag _flag ← False_ 

- 3: **while** _flag_ **do** 

- 4: **for** _a ∈ A_ **do** 

- 5: Update solution _x_ according to _a_ ; _▷_ Action thought application with heuristic methods 

- 6: **for** _s ∈ S_ **do** 

- 7: Display state _s_ ; _▷_ State thought application 

- 8: **end for** 

- 9: Update instance _I_ ; 

- 10: **end for** 

- 11: Update _flag_ ; _▷_ Update the iteration condition 12: **end while** 

### **3.3 Backward MTP Framework** 

High-quality GCO solutions often embed intelligent problem solving strategies. Although some established knowledge has guided heuristic and approximation algorithm design, many complex patterns remain undiscovered due to analytical complexity. The representational capacity of deep networks enables them to encode such optimal solution patterns, making it promising to generate thoughts for LLMs using approximation or optimal solvers’ guidance. 

The red-highlighted modules in Figure 2 structurally define the backward MTP framework. This architecture employs high-quality solvers (including both exact and approximate methods) to obtain high-quality solutions from which we can extract solution construction patterns. The action thought set is constrained to a single operator, AddOne, which incrementally incorporates solution elements 

5 

into the current partial solution, thereby generating stepwise trajectories. The state design methodology maintains consistency with the forward framework in Section 3.2. The program _P_ integrates a task-specific solver _X_ with the thought-generation process through the Program Template 2. An application of the backward MTP framework for the MIS problem is shown in Appendix H.2. 

**Program 2** A Backward MTP Program Template **Require:** Instance _I_ , action thought set _A_ , state thought set _S_ , a solver _X_ of _τ_ . 

- 1: Initialize an optimal or suboptimal solution _x_ ˆ _←X_ ( _I_ ) 

- 2: Initialize an empty solution _x ←∅_ 

- 3: Initialize a solving flag _flag ← False_ 

- 4: **while** _flag_ **do** 

- 5: _e ←_ AddOne(ˆ _x_ ); _▷_ Add element from standard solution 

- 6: _x ← x ∪{e}_ ; 

- 7: **for** _s ∈ S_ **do** 

- 8: Display state _s_ ; _▷_ State thought application 

- 9: **end for** 

- 10: Update instance _I_ ; 

- 11: Update _flag_ ; _▷_ Update the iteration condition 

- 12: **end while** 

## **4 Experiments** 

With generated reasoning datasets, we fine-tuned Meta-Llama-3-8B-Instruct<sup>2</sup> using Low-Rank Adaptation (LoRA) via the llama-factory framework<sup>3</sup> , naming the resulting model **Llama-GT** (GT means GraphThought). For inference, we use vLLM<sup>4</sup> to accelerate. Full hyperparameters are placed in Appendix B. For performance evaluation, we adopted the _optimality_ metric from the GraphArena benchmark (Tang et al., 2025). Regarding the definitions of small/large graphs, we strictly followed the specifications in GraphArena: i) **Neighbor/Distance Task** : Small (contains 4-19 nodes), Large (contains 20-50 nodes); ii) **Connected/Diameter/MCP/MIS/MVC Task** : Small (contains 4-14 nodes), Large (contains 15-30 nodes); iii) **MCS/GED/TSP Task** : Small (contains 4-9 nodes), Large (contains 10-20 nodes). 

The evaluation covered all ten predefined tasks in GraphArena, with detailed task descriptions and 

> 2https://huggingface.co/meta-llama/ Meta-Llama-3-8B-Instruct 

optimality criteria provided in Appendix B.3. **Comparison with Original GraphArena** . We present the majority of GraphArena’s original results in Appendix E, retaining only the key comparisons with DeepSeek-V2-Coder, GPT4o-Coder, and Qwen2-7B-SFT. While codeaugmented approaches (DeepSeek-V2-Coder and GPT-4o-Coder) demonstrate intermediate performance on fundamental tasks, they exhibit limitations when confronted with complex challenges such as graph diameter computation (0 _._ 334 optimality rate), which Llama-GT effectively addresses (0 _._ 954). Notably, Qwen2-7B-SFT achieves strong performance on basic operations but fails catastrophically on MIS for large graphs (0 _._ 054), underscoring the constraints of supervised fine-tuning without a thought-enhanced paradigm. 

**Comparison with Few-shot Thought Prompting** . While few-shot prompting improves performance, Llama-GT shows greater consistency, especially on large graphs. DeepSeek-V3 achieves perfect scores on simple tasks like Neighbor (1 _._ 0) but struggles with MVC (0 _._ 366). Llama-GT outperforms DeepSeek-V3 on NP-hard tasks like MVC (0 _._ 744 vs 0 _._ 120) and MIS (0 _._ 900 vs 0 _._ 304), demonstrating the superiority of the GraphThought framework over few-shot exemplars. 

**Comparison with STaR Framework** . Comparison with the STaR (Zelikman et al., 2022) framework’s self-generated thought approach reveals critical insights. Using STaR with Llama-38B-Instruct under two configurations<sup>5</sup> : (1) fewshot prompting with thoughts generated with our GraphThought framework and (2) with LLMgenerated thoughts. Llama-GT substantially outperforms both variants across all graph sizes, showing 2-3x improvements on large graphs (MVC: 0 _._ 744 vs 0 _._ 360, MIS: 0 _._ 900 vs 0 _._ 216). The gap persists even when STaR uses our thoughtenhanced examples, emphasizing the limits of iterative self-improvement approaches. In addition, STaR(w/GT) performs better than STaR(w/LLM) across nearly all tasks and different graph sizes, further underscoring the importance of our thought paradigm over automated generation for training. **Ablation of Thought Mechanism Impact** The thought mechanism significantly improves performance on NP-hard tasks. Llama-GT without thought integration still performs well on polynomial tasks (e.g., Neighbor: 0 _._ 988 small, 0 _._ 804 

> 3https://github.com/hiyouga/LLaMA-Factory 

> 4https://github.com/vllm-project/vllm 

> 5More detailed configuations see appendix B. 

6 

Table 1: Performance comparison of optimal solution rates (%) across 10 graph tasks, evaluated on small and large graphs, each has 500 instances. Results are shown for: (1) Code-augmented models (DeepSeek-V2-Coder, GPT-4o-Coder) and Supervised Fine-Tuned Model provided by GraphArena (Qwen2-7B-SFT);(2) Few-shot thought prompting variants (Deepseek-V3, Llama-3.3-70B, etc.); (3) STaR framework implementations with different fewshot strategies; and (4) Llama-GT trained with/without thought mechanisms. Metrics include polynomial tasks (Neighbor, Distance, Connected, Diameter), NP-hard tasks (MVC, MIS, MCP, TSP, MCS, GED).<sup>_∗_</sup> indicates that the model in the GraphArena was trained on fewer data compared to the data used in our model. 

||||Gra|ph Task (Sm|all Graphs)||||||
|---|---|---|---|---|---|---|---|---|---|---|
|Model|Neighbor|Distance|Connected|Diameter|MVC|MIS|MCP|TSP|MCS|GED|
|DeepSeek-V2-Coder|0.816|0.894|0.586|0.142|0.176|0.482|0.498|0.276|0.228|0.214|
|GPT-4o-Coder|0.808|0.654|0.712|0.334|0.296|0.530|0.644|**0.490**|0.508|0.320|
|Qwen2-7b-SFT<sup>_∗_</sup>|0.966|0.912|0.888|0.608|0.548|0.702|0.696|0.368|0.000|0.054|
|+Few-shot Thought|||||||||||
|Deepseek-V3|**1.000**|0.988|**1.000**|0.850|0.366|0.642|0.754|0.370|**0.544**|0.308|
|Llama-3.3-70B|0.970|0.970|0.954|0.674|0.206|0.648|0.554|0.292|0.484|0.326|
|Mixtral-8x7b|0.580|0.536|0.378|0.156|0.148|0.326|0.490|0.168|0.196|0.262|
|Llama3-8b-Instruct|0.700|0.480|0.502|0.070|0.108|0.248|0.258|0.190|0.222|0.450|
|+SFT|||||||||||
|STaR(w/ GT)|0.648|0.910|0.522|0.466|0.722|0.640|0.676|0.352|0.308|0.370|
|STaR(w/ LLM)|0.296|0.662|0.440|0.380|0.688|0.654|0.288|0.282|0.328|0.258|
|**Llama-GT(w/o Thought)**|0.988|0.990|0.906|0.820|0.930|0.972|0.906|0.366|0.538|**0.608**|
|**Llama-GT**|**1.000**|**1.000**|0.996|**0.954**|**0.972**|**0.994**|**0.952**|0.392|0.496|0.460|
||||Gra|ph Task (Lar|ge Graphs)||||||
|Model|Neighbor|Distance|Connected|Diameter|MVC|MIS|MCP|TSP|MCS|GED|
|DeepSeek-V2-Coder|0.672|0.632|0.206|0.008|0.080|0.028|0.072|0.000|0.022|0.014|
|GPT-4o-Coder|0.868|0.684|0.378|0.112|0.110|0.072|0.222|0.028|**0.036**|0.018|
|Qwen2-7b-SFT<sup>_∗_</sup>|0.790|0.570|0.230|0.092|0.156|0.054|0.136|0.000|0.000|0.032|
|+Few-shot Thought|||||||||||
|DeepSeek-V3|**0.992**|0.942|**0.932**|0.448|0.120|0.304|0.290|0.020|0.012|0.020|
|Llama-3.3-70B|0.952|0.866|0.856|0.290|0.118|0.254|0.136|0.000|0.012|0.012|
|Mixtral-8x7b|0.466|0.282|0.108|0.002|0.032|0.024|0.056|0.000|0.000|0.022|
|Llama3-8b-Instruct|0.604|0.220|0.132|0.002|0.028|0.010|0.038|0.000|0.002|0.026|
|+SFT|||||||||||
|STaR(w/ GT)|0.374|0.618|0.124|0.080|0.360|0.216|0.134|0.018|0.006|0.026|
|STaR(w/ LLM)|0.320|0.332|0.090|0.038|0.126|0.124|0.030|0.002|0.004|0.024|
|**Llama-GT(w/o Thought)**|0.804|0.864|0.340|0.302|0.652|0.652|0.370|0.024|0.020|**0.068**|
|**Llama-GT**|0.988|**0.984**|0.836|**0.600**|**0.744**|**0.900**|**0.634**|**0.036**|**0.036**|0.008|



large). With thought integration, MVC increases from 0 _._ 930 to 0 _._ 972 (small) and 0 _._ 652 to 0 _._ 744 (large), MIS from 0 _._ 972 to 0 _._ 994 (small) and 0 _._ 652 to 0 _._ 900 (large). However, performance drops on GED (small: 0 _._ 608 to 0 _._ 460; large: 0 _._ 068 to 0 _._ 008). We posit that potential causes underlying this phenomenon will be explored in the later discussion. **Performance Comparison on Reasoning** . We conducted a comprehensive performance comparison between Llama-GT and two state-of-the-art inference models: QWQ-32B and DeepSeek-R1Distill-Llama-8B. All models were evaluated on 500 instances per task using vLLM with identical experimental configurations. As demonstrated in Figure 3, Llama-GT achieves comparable or superior performance to both baseline models across polynomial-time tasks and specific NP-hard problems, particularly excelling in MVC and MIS tasks. 

Our analysis reveals a critical efficiency advantage: conventional inference models exhibit 

prolonged cognitive processing phases during problem-solving, often generating redundant computational steps that exceed the maximum token threshold, resulting in significantly slower inference speeds. In contrast, our trained model constrains these cognitive mechanisms to operate within fixed patterns, achieving substantial time efficiency improvements while maintaining solution quality as shown in Figure 3. 

However, performance disparities persist in more complex CO tasks such as TSP, Graph Edit Distance (GED), and Maximum Common Subgraph (MCS). We provide complete quantitative results and a systematic analysis of these performance degradation patterns in Appendix J. 

**BoN-Enhanced Optimality Rates versus Heuristics** . We introduce a generalized optimality ratio metric for evaluating the quality of a found solution given an instance. For each problem instance _I_ , the optimal solution _x_<sup>_∗_</sup> is obtained using Gurobi, 

7 



Figure 3: Performance and time cost of inference model and Llama-GT on ten graph tasks of GraphArena benchmark. (Upper-Left) Performance on small graph instances. (Upper-Right) Performance on large ones. (Bottom-Left) Inference time cost on small ones. (Bottom-Right) Inference time cost on large ones. 

which guarantees exact optimality. The optimality ratio for a solution _x_ on the instance _I_ of a GCO problem _τ_ is formally defined as: 



where _ϕ_ ( _·_ ) is the evaluation function of the solution of _τ_ . This symmetric ratio works for both maximization and minimization tasks. For maximization tasks (e.g., MIS), where _ϕ_ ( _x_ ) _≤ ϕ_ ( _x_<sup>_∗_</sup> ), the ratio<sup>_<u>ϕ</u>_</sup><sup><u>(</u></sup><sup>_x_</sup><sup><u>)</u></sup> _ϕ_ ( _x_<sup>_<u>∗</u>_</sup> )<sup>directly measures approximation qual-</sup> ity within [0 _,_ 1]. For minimization problems (e.g., MVC), the inverse ratio<sup>_<u>ϕ</u>_</sup><sup><u>(</u></sup><sup>_x∗_</sup><sup><u>)</u></sup> _ϕ_ ( _x_ )<sup>appropriately penal-</sup> izes suboptimal solutions while maintaining the same normalized range. This metric enables crossproblem performance comparisons while maintaining the interpretability of near-optimal solutions. 

Figure 4 demonstrates the average optimality ratio through comprehensive evaluations across 1 _,_ 000 graph instances (500 small and 500 large) spanning 6 NP-Hard tasks: GED, MCP, MCS, MIS, MVC and TSP. Our base model ( _n_ = 1, without Best-of- _N_ enhancement) achieves remarkable optimality ratios of 93 _._ 9% on small graphs and 79 _._ 1% on large graphs, outperforming random baselines by significant margins of 1 _._ 9% and 20 _._ 7% respectively. These results demonstrate the inherent effectiveness of our Llama-GT model in generalizing across problem scales and types. 



Figure 4: Average performance of Llama-GT with BoN strategy and classic solvers on 6 NP-Hard Tasks (GED, MCP, MCS, MIS, MVC, TSP) for small and large graphs. The values represent the average optimality ratio across different tasks. 

We enhance solution quality with the Best-of-N (BoN) strategy, which generates _n_ candidate solutions per instance and selects the best. With BoN(n=32), optimality improves to 98.7% on small graphs and 88 _._ 4% on large graphs, surpassing greedy algorithms (96 _._ 3% and 87 _._ 9%, respectively). This technique significantly narrows the performance gap between data-driven approaches and manual heuristics, achieving near-optimal results without problem-specific rules. 

A case study in the MIS problem (Figure 1) highlights our approach’s superiority. While the greedy algorithm selects low-degree nodes (e.g., node 16), our method uses adaptive heuristics to prioritize high-impact nodes (e.g., node 18) and optimize selections based on evolving graph structures, achieving a 12-node MIS compared to the greedy algorithm’s 11. This demonstrates how our framework avoids the myopic decisions of traditional heuristics, leading to higher-quality solutions. 

## **5 Conclusion** 

We introduce **GraphThought** , a structured framework for improving the reasoning capabilities of LLM on GCO problems. By formalizing the OTD problem, we enable the construction of high-quality reasoning trajectories via two distinct data generation strategies: a heuristic-driven forward method for polynomial-time tasks, and a solver-aligned backward method for NP-hard problems. Finetuning LLMs with these structured trajectories yields Llama-GT, a compact 8B-parameter model that achieves state-of-the-art performance on the GraphArena benchmark, surpassing significantly larger models across multiple GCO tasks. These results suggest that incorporating structured reasoning into LLM training holds substantial potential 

8 

for advancing CO with language-based models. 

## **6 Limitations** 

Despite the promising results achieved by GraphThought framework, several important limitations remain, which are outlined below. 

**Performance on Complex or Knowledge-Scarce Problems.** While the proposed framework significantly enhances the reasoning capabilities of large language models (LLMs) through structured reasoning, its performance deteriorates when applied to problems of significantly higher complexity or those lacking explicit combinatorial priors—such as the Traveling Salesman Problem (TSP), Graph Edit Distance (GED), and Maximum Common Subgraph (MCS)—as discussed in Section J. These challenges are particularly pronounced in NP-hard graph optimization tasks that require long reasoning chains or lack clear heuristic guidance. 

**Efficiency Concerns of LLM-Based Solvers.** Employing large language models as combinatorial problem solvers inherently introduces computational inefficiencies. Compared to traditional optimization solvers like Gurobi or specialized heuristic algorithms, LLM-based approaches suffer from higher inference latency and substantial computational resource demands. This inefficiency limits their practical deployment, particularly in scenarios requiring rapid or real-time responses. 

**Difficulty in Scaling to Large Graph Instances.** A crucial limitation arises from the inability of our method to efficiently address large-scale graph instances. Due to the verbose and sequential nature of natural language reasoning employed by LLMs, handling large graphs—comprising thousands or millions of nodes—poses significant representation and computational challenges. These large graph instances typically exceed the context length of current LLM architectures, resulting in fragmented or incomplete reasoning processes and thus severely compromising solution quality and validity. 

In summary, while our GraphThought framework demonstrates substantial improvements in LLM capabilities for GCO, addressing the aforementioned limitations remains a vital direction for future research. 

9 

## **References** 

- Anonymous. 2024. Solving diverse combinatorial optimization problems with a unified model. In _Submitted to ICLR_ . Under review. 

- Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, and 1 others. 2024a. Graph of thoughts: Solving elaborate problems with large language models. In _AAAI_ . 

- Maciej Besta, Florim Memedi, Zhenyu Zhang, Robert Gerstenberger, Guangyuan Piao, Nils Blach, Piotr Nyczyk, Marcin Copik, Grzegorz Kwasniewski, Jürgen Müller, and 1 others. 2024b. Demystifying chains, trees, and graphs of thoughts. _arXiv:2401.14295_ . 

- Yukun Cao, Shuo Han, Zengyi Gao, Zezhong Ding, Xike Xie, and S Kevin Zhou. 2024. Graphinsight: Unlocking insights in large language models for graph structure understanding. _arXiv:2409.03258_ . 

- Ziwei Chai, Tianjie Zhang, Liang Wu, Kaiqiao Han, Xiaohai Hu, Xuanwen Huang, and Yang Yang. 2023. Graphllm: Boosting graph reasoning ability of large language model. _arXiv:2310.05845_ . 

- Lijun Chang, Wei Li, and Wenjie Zhang. 2017. Computing a near-maximum independent set in linear time by reducing-peeling. In _Proceedings of the 2017 ACM International Conference on Management of Data_ , pages 1181–1196. 

- Nuo Chen, Yuhan Li, Jianheng Tang, and Jia Li. 2024a. Graphwiz: An instruction-following language model for graph computational problems. In _KDD_ . 

- Zhikai Chen, Haitao Mao, Hang Li, Wei Jin, Hongzhi Wen, Xiaochi Wei, Shuaiqiang Wang, Dawei Yin, Wenqi Fan, Hui Liu, and 1 others. 2024b. Exploring the potential of large language models (LLMs) in learning on graphs. _ACM SIGKDD Explorations Newsletter_ , 25(2):42–61. 

- Xinnan Dai, Qihao Wen, Yifei Shen, Hongzhi Wen, Dongsheng Li, Jiliang Tang, and Caihua Shan. 2024. Revisiting the graph reasoning ability of large language models: Case studies in translation, connectivity and shortest path. _arXiv:2408.09529_ . 

- Darko Drakulic, Sofia Michel, and Jean-Marc Andreoli. 2024. Goal: A generalist combinatorial optimization agent learner. _arXiv:2406.15079_ . 

- Mohammed Elhenawy, Ahmed Abdelhay, Taqwa I Alhadidi, Huthaifa I Ashqar, Shadi Jaradat, Ahmed Jaber, Sebastien Glaser, and Andry Rakotonirainy. 2024a. Eyeballing combinatorial problems: A case study of using multimodal large language models to solve traveling salesman problems. _arXiv:2406.06865_ . 

- Mohammed Elhenawy, Ahmad Abutahoun, Taqwa I Alhadidi, Ahmed Jaber, Huthaifa I Ashqar, Shadi Jaradat, Ahmed Abdelhay, Sebastien Glaser, and Andry 

Rakotonirainy. 2024b. Visual reasoning and multiagent approach in multimodal large language models (mllms): Solving tsp and mtsp combinatorial challenges. _arXiv:2407.00092_ . 

- Bahare Fatemi, Jonathan Halcrow, and Bryan Perozzi. 2023. Talk like a graph: Encoding graphs for large language models. _arXiv:2310.04560_ . 

- Yifan Feng, Chengwu Yang, Xingliang Hou, Shaoyi Du, Shihui Ying, Zongze Wu, and Yue Gao. 2024. Beyond graphs: Can large language models comprehend hypergraphs? _arXiv:2410.10083_ . 

- Hamed Firooz, Maziar Sanjabi, Wenlong Jiang, and Xiaoling Zhai. 2024. Lost-in-distance: Impact of contextual proximity on llm performance in graph tasks. _arXiv:2410.01985_ . 

- Kanishk Gandhi, Denise Lee, Gabriel Grand, Muxin Liu, Winson Cheng, Archit Sharma, and Noah D Goodman. 2024. Stream of search (sos): Learning to search in language. _arXiv:2404.03683_ . 

- Jiayan Guo, Lun Du, Hengyu Liu, Mengyu Zhou, Xinyi He, and Shi Han. 2023. Gpt4Graph: Can large language models understand graph structured data? an empirical evaluation and benchmarking. _arXiv:2305.15066_ . 

- Yuwei Hu, Runlin Lei, Xinyi Huang, Zhewei Wei, and Yongchao Liu. 2024. Scalable and accurate graph reasoning with llm-based multi-agents. _arXiv:2410.05130_ . 

- Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024. Large language models cannot self-correct reasoning yet. In _ICLR_ . 

- S. Iklassov, J. Smith, and K. Lee. 2024. Deep learning approaches for graph combinatorial optimization problems. _Journal of Artificial Intelligence Research_ , 70:123–145. 

- Xia Jiang, Yaoxin Wu, Yuan Wang, and Yingqian Zhang. 2024a. Unco: Towards unifying neural combinatorial optimization through large language model. _arXiv:2408.12214_ . 

- Zhengdao Jiang, Zhen Zhang, Yujia Li, and Jure Leskovec. 2024b. Graph neural networks for combinatorial optimization: A survey. In _Proceedings of the 38th AAAI Conference on Artificial Intelligence_ . 

- Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, and Jiawei Han. 2024a. Large language models on graphs: A comprehensive survey. _IEEE Transactions on Knowledge and Data Engineering_ . 

- Xiaoyang Jin, Yujie Fan, Yujia Li, and Jure Leskovec. 2024b. Learning to solve combinatorial optimization problems on graphs via reinforcement learning. In _Proceedings of the 38th AAAI Conference on Artificial Intelligence_ . 

10 

- L. R. Ford Jr. and D. R. Fulkerson. 1956. Maximal flow through a network. _Canadian Journal of Mathematics_ , 8:399–404. 

- Joseph B. Kruskal. 1956. On the shortest spanning subtree of a graph and the traveling salesman problem. _Proceedings of the American Mathematical Society_ , 7(1):48–50. 

- Harold W. Kuhn. 1955. The hungarian method for the assignment problem. In _Naval Research Logistics Quarterly_ , volume 2, pages 83–97. 

- Lucas Lehnert, Sainbayar Sukhbaatar, Paul McVay, Michael Rabbat, and Yuandong Tian. 2024a. Beyond a*: Better planning with transformers via search dynamics bootstrapping. In _ICLR Workshop on Large Language Model (LLM) Agents_ . 

- T. Lehnert, A. Müller, and Y. Zhang. 2024b. Graph neural networks for solving np-hard problems: A review. _IEEE Transactions on Neural Networks and Learning Systems_ , 35(4):789–805. 

- H. Li, S. Wang, and T. Zhang. 2024a. Text-based approaches to graph combinatorial problems using large language models. _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 456–467. 

- J. Li, N. Chen, and Q. Zhang. 2024b. Optimal thoughts design for graph combinatorial optimization. _arXiv preprint arXiv:2406.07890_ . 

- Xin Li, Qizhi Chu, Yubin Chen, Yang Liu, Yaoqi Liu, Zekai Yu, Weize Chen, Chen Qian, Chuan Shi, and Cheng Yang. 2024c. Graphteam: Facilitating large language model-based graph analysis via multi-agent collaboration. _arXiv:2410.18032_ . 

- Jiawei Liu, Cheng Yang, Zhiyuan Lu, Junze Chen, Yibo Li, Mengmei Zhang, Ting Bai, Yuan Fang, Lichao Sun, Philip S Yu, and 1 others. 2023a. Towards graph foundation models: A survey and beyond. _arXiv:2310.11829_ . 

- Y. Liu, X. Chen, and Y. Zhao. 2023b. Benchmarking large language models on graph problems. _arXiv preprint arXiv:2309.01234_ . 

- Yujie Liu, Yujia Li, and Jure Leskovec. 2023c. Combinatorial optimization with graph neural networks: A survey. _arXiv preprint arXiv:2301.11270_ . 

- Michael Luby. 1986. A simple parallel algorithm for the maximal independent set problem. _SIAM Journal on Computing_ , 15(4):1036–1053. 

- Z. Luo, X. Song, H. Huang, J. Lian, C. Zhang, J. Jiang, X. Xie, and H. Jin. 2024a. Graphinstruct: Empowering large language models with graph understanding and reasoning capability. _arXiv preprint arXiv:2403.04483_ . 

- Zihan Luo, Xiran Song, Hong Huang, Jianxun Lian, Chenhao Zhang, Jinqi Jiang, Xing Xie, and Hai Jin. 2024b. Graphinstruct: Empowering large language models with graph understanding and reasoning capability. _arXiv:2403.04483_ . 

- L. Ouyang, J. Wu, and Y. Zhang. 2024a. Enhancing llms for graph reasoning tasks. _arXiv preprint arXiv:2402.09876_ . 

- Sheng Ouyang, Yulan Hu, Ge Chen, and Yong Liu. 2024b. Gundam: Aligning large language models with graph understanding. _arXiv:2409.20053_ . 

- Vangelis Th Paschos. 2014. _Applications of Combinatorial Optimization_ . John Wiley & Sons. 

- Bryan Perozzi, Bahare Fatemi, Dustin Zelle, Anton Tsitsulin, Mehran Kazemi, Rami Al-Rfou, and Jonathan Halcrow. 2024. Let your graph do the talking: Encoding structured data for LLMs. _arXiv:2402.05862_ . 

- Xubin Ren, Jiabin Tang, Dawei Yin, Nitesh Chawla, and Chao Huang. 2024a. A survey of large language models for graphs. In _KDD_ . 

- Y. Ren, L. Zhao, and M. Chen. 2024b. Large language models for combinatorial optimization: Opportunities and challenges. _arXiv preprint arXiv:2401.12345_ . 

- Clayton Sanford, Bahare Fatemi, Ethan Hall, Anton Tsitsulin, Mehran Kazemi, Jonathan Halcrow, Bryan Perozzi, and Vahab Mirrokni. 2024a. Understanding transformer reasoning capabilities via graph algorithms. _arXiv:2405.18512_ . 

- J. Sanford, D. Lee, and H. Kim. 2024b. Meta-thought programming: A framework for dual-mode reasoning in llms. _arXiv preprint arXiv:2405.06789_ . 

- C. Skianis, D. Papadopoulos, and G. Karypis. 2024a. Graphthought: Structured reasoning for graph problems with large language models. _arXiv preprint arXiv:2404.05678_ . 

- Konstantinos Skianis, Giannis Nikolentzos, and Michalis Vazirgiannis. 2024b. Graph reasoning with large language models via pseudo-code prompting. _arXiv:2409.17906_ . 

- Jianheng Tang, Qifan Zhang, Yuhan Li, Nuo Chen, and Jia Li. 2025. Grapharena: Evaluating and exploring large language models on graph computation. In _The Thirteenth International Conference on Learning Representations_ . 

- Heng Wang, Shangbin Feng, Tianxing He, Zhaoxuan Tan, Xiaochuang Han, and Yulia Tsvetkov. 2024a. Can language models solve graph problems in natural language? In _NeurIPS_ . 

- Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2022. Self-consistency improves chain of thought reasoning in language models. _arXiv preprint arXiv:2203.11171_ . 

11 

- Yiming Wang, Ziyang Zhang, Hanwei Chen, and Huayi Shen. 2024b. Reasoning with large language models on graph tasks: The influence of temperature. In _ICCEA_ . 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. 2022. Chain-of-thought prompting elicits reasoning in large language models. In _NeurIPS_ . 

- Yanbin Wei, Shuai Fu, Weisen Jiang, James T Kwok, and Yu Zhang. 2024. Gita: Graph to visual and textual integration for vision-language graph reasoning. _arXiv:2402.02130_ . 

- Tianhao Wu, Janice Lan, Weizhe Yuan, Jiantao Jiao, Jason Weston, and Sainbayar Sukhbaatar. 2024. Thinking llms: General instruction following with thought generation. _arXiv:2410.10630_ . 

- Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2024. Tree of thoughts: Deliberate problem solving with large language models. In _NeurIPS_ . 

- Zike Yuan, Ming Liu, Hui Wang, and Bing Qin. 2024. Gracore: Benchmarking graph comprehension and complex reasoning in large language models. _arXiv:2407.02936_ . 

- Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. 2022. Star: Bootstrapping reasoning with reasoning. In _NeurIPS_ . 

- Yizhuo Zhang, Heng Wang, Shangbin Feng, Zhaoxuan Tan, Xiaochuang Han, Tianxing He, and Yulia Tsvetkov. 2024. Can llm graph reasoning generalize beyond pattern memorization? _arXiv:2406.15992_ . 

12 

## **A Related Work** 

### **A.1 LLMs for Graph Combinatorial Optimization** 

The integration of Large Language Models (LLMs) into solving Graph Combinatorial Optimization (GCO) problems has garnered significant attention in recent years. Several works have attempted to leverage LLMs for GCO problems from various perspectives. Jin et al. (Jin et al., 2024a) provided a comprehensive survey on the application of LLMs on graphs, categorizing potential scenarios into pure graphs, text-attributed graphs, and text-paired graphs. They discussed techniques such as using LLMs as predictors, encoders, and aligners. Chen et al. (Chen et al., 2024b) explored the potential of LLMs in graph machine learning, especially for node classification tasks, and investigated two pipelines: LLMs-as-Enhancers and LLMs-as-Predictors. Liu et al. (Liu et al., 2023a) introduced the concept of Graph Foundation Models (GFMs) and classified existing work into categories based on their dependence on graph neural networks and LLMs. Ren et al. (Ren et al., 2024a) conducted a survey on LLMs for graphs, proposing a taxonomy to categorize existing methods based on their framework design. 

### **A.1.1 Prompt Engineering and Benchmark Development** 

Recent advances in LLM applications for graph problems have focused on prompt engineering strategies and comprehensive benchmarking frameworks. Wang et al. (Wang et al., 2024a) introduced the NLGraph benchmark with Build-a-Graph prompting and algorithmic optimizations for graph reasoning tasks. Tang et al. (Tang et al., 2025) developed GraphArena as a standardized benchmarking platform, while Yuan et al. (Yuan et al., 2024) proposed GraCoRe for assessing graph comprehension capabilities. Skianis et al. (Skianis et al., 2024b) demonstrated the effectiveness of pseudo-code prompting for enhancing graph problem performance. 

### **A.1.2 Architectural and Framework Innovations** 

Several architectural innovations have emerged to enhance LLM capabilities in graph processing. Li et al. (Li et al., 2024c) introduced GraphTeam as a multi-agent collaborative system, complemented by Hu et al.’s GraphAgent-Reasoner framework (Hu et al., 2024). Perozzi et al. (Perozzi et al., 2024) developed GraphToken for explicit structured data representation, while Cao et al. (Cao et al., 2024) proposed GraphInsight to improve structural comprehension. 

### **A.1.3 Graph Representation and Encoding Strategies** 

Innovative graph encoding methods have been crucial for bridging the gap between LLMs and graph structures. Fatemi et al. (Fatemi et al., 2023) pioneered text-based graph encoding, while Elhenawy et al. (Elhenawy et al., 2024a,b) explored multimodal visual reasoning for TSP solutions. Feng et al. (Feng et al., 2024) extended these approaches to hypergraphs through LLM4Hypergraph. 

### **A.1.4 Empirical Analysis and Performance Factors** 

Comprehensive empirical studies have revealed critical insights into LLM capabilities and limitations. Guo et al. (Guo et al., 2023) conducted large-scale evaluations on graph-structured data, while Wang et al. (Wang et al., 2024b) analyzed temperature’s impact on reasoning performance. Firooz et al. (Firooz et al., 2024) investigated contextual proximity effects, and Dai et al. (Dai et al., 2024) provided case studies on graph reasoning limitations. Sanford et al. (Sanford et al., 2024a) analyzed transformer architectures through graph algorithmic lenses. 

Other works have focused on training graph foundation models using dense embeddings from LLM pretraining. Drakulic et al. (Drakulic et al., 2024) proposed GOAL, a generalist model for solving multiple combinatorial optimization problems. Jiang et al. (Jiang et al., 2024a) introduced UNCO, a unified framework for solving various COPs using LLMs. Anonymous (Anonymous, 2024) proposed a unified model for diverse CO problems using a transformer backbone. Chai et al. (Chai et al., 2023) introduced GraphLLM to boost the graph reasoning ability of LLMs. Wei et al. (Wei et al., 2024) proposed GITA, a framework integrating visual and textual information for graph reasoning. 

13 

### **A.2 Chain-of-Thought, Tree-of-Thought, and Graph-of-Thought Methods** 

The Chain-of-Thought (CoT) prompting technique, introduced by Wei et al. (Wei et al., 2022), demonstrates that generating intermediate reasoning steps can significantly improve LLMs’ performance on complex reasoning tasks. This method was further extended by Yao et al. (Yao et al., 2024), who proposed the Tree of Thoughts (ToT) framework, enabling exploration over coherent units of text (thoughts) to enhance problem-solving abilities. The ToT approach allows LMs to consider multiple reasoning paths and self-evaluate choices, significantly improving performance on tasks requiring non-trivial planning or search. Besta et al. (Besta et al., 2024a) introduced the Graph of Thoughts (GoT), which advances prompting capabilities by modeling LLM-generated information as an arbitrary graph. This approach enables combining arbitrary LLM thoughts into synergistic outcomes and enhances thoughts using feedback loops. Besta et al. (Besta et al., 2024b) further demystified the concepts of chains, trees, and graphs of thoughts, providing a taxonomy of structure-enhanced LLM reasoning schemes. These studies highlight the importance of structured reasoning topologies in improving LLMs’ problem-solving abilities. 

### **A.3 Self-Correction, Planning, and Search Strategy Learning** 

Huang et al. (Huang et al., 2024) examined the role of self-correction in LLMs, finding that intrinsic self-correction without external feedback often fails to improve reasoning accuracy. In contrast, Lehnert et al. (Lehnert et al., 2024a) proposed the Searchformer model, which predicts the search dynamics of the A* algorithm, significantly outperforming traditional planners on complex decision-making tasks. Gandhi et al. (Gandhi et al., 2024) introduced the Stream of Search (SoS) approach, teaching language models to search by representing the process as a flattened string. This method significantly improved search accuracy and enabled flexible use of different search strategies. 

## **B Experiments Setting** 

### **B.1 Training Parameter** 

Our framework is implemented based on LLaMA-Factory. We perform supervised fine-tuning (SFT) on the Meta-Llama-3-8B-Instruct<sup>6</sup> model using LoRA adaptation. The training process is conducted on a NVIDIA H800 PCIe 80GB GPU with 30K instruction-following examples. Key hyperparameters include a cosine learning rate scheduler with initial value 8e-4, 4 training epochs, and gradient accumulation over 8 steps. The complete configuration details are presented in Table 2. 

We follow the dataset construction methodology described in the original STaR(Zelikman et al., 2022) paper. Specifically, we first perform inference using either an untrained or partially trained model, then conduct rationalization on unsuccessful cases that failed to reach the optimal solution. After collecting these rationalized examples to construct the training dataset, we subsequently perform supervised finetuning (SFT) on the base model. For the base model, we consistently employ Llama-3-8B-Instruct with identical hyperparameter settings as listed in the configuration Table 2. The complete STaR process undergoes four iterative cycles to progressively enhance model performance. 

### **B.2 Inference Setting** 

During the inference phase, we deployed the base untrained and trained model using the vllm framework, including Llama-GT, the original Meta-Llama-3-8B-Instruct model and the reasoning models (QWQ-32B<sup>7</sup> and DeepSeek-R1-Distill-Llama-8B<sup>8</sup> ). Other models utilized API-based inference (including DeepseekV3,<sup>9</sup> , llama-3.3-70b, mixtral-8x7b and QwQ-32B-Preview<sup>10</sup> ). To ensure reproducibility, we configured the temperature parameter to 0.1 for all models. Due to computational constraints, each API-based model underwent single-pass inference for each test instance. 

> 6https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct 

> 7https://huggingface.co/Qwen/QwQ-32B 

> 8https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B 

> 9https://api.deepseek.com 

> 10https://api.pandalla.ai/ 

14 

Table 2: Training Configuration 

|**Category**|**Setting**|
|---|---|
|**Model Configuration**||
|Base Model|Llama-3-8B-Instruct|
|Fine-tuning Method|LoRA|
|Hardware|a NVIDIA H800 PCIe 80GB GPU|
|Dataset Size|30,000 samples|
|Validation Split|10%|
|Max Sequence Length|3,000 tokens|
|**Training Parameters**||
|Epochs|4|
|Learning Rate|8e-4|
|Batch Size (per device)|8|
|Gradient Accumulation Steps|8|
|Optimizer|AdamW|
|Learning Rate Scheduler|Cosine|
|Warmup Steps|0|
|Max Gradient Norm|1.0|
|**LoRA Configuration**||
|LoRA Rank|8|
|LoRA Alpha|16|
|LoRA Dropout|0|



For Best-of-N(BoN) experiments investigating whether increased inference-time computation enhances model performance, we adjusted the batch size to 16 or 32 while maintaining a temperature setting of 1.0 to maximize response diversity. 

### **B.3 Evaluation Dataset** 

We conduct evaluations using GraphArena’s original test datasets with preserved graph size definitions ("small" vs "large") from their benchmark. The 10 tasks are categorized by time complexity and specified as follows: 

- **Common Neighbor (Polynomial)** : For graph _G_ = _{V, E}_ and nodes _v_ 1 _, v_ 2, identify all _u ∈V_ connecting to both. Optimal solution maximizes _|S|_ where _S_ = _{u |_ ( _u, v_ 1) _,_ ( _u, v_ 2) _∈E}_ . **Neighbor** for short. 

- **Shortest Distance (Polynomial)** : Find the path between _v_ 1 and _v_ 2 with minimal hops in _G_ . Optimality requires min _ℓ_ ( _pv_ 1 _→v_ 2). **Distance** for short. 

- **Connected Component (Polynomial)** : Select representative nodes covering all components. Optimality demands full coverage ( _|C|_ = total components). **Connected** for short. 

- **Graph Diameter (Polynomial)** : Identify the longest shortest path. The optimal solution achieves max _u,v d_ ( _u, v_ ). **Diameter** for short. 

- **Maximum Clique Problem (NP-hard)** : A clique is a complete subgraph where every pair of distinct vertices is connected. The task requires identifying the largest such subgraph _C ⊆V_ in _G_ . A solution is optimal if no larger clique exists in the graph (i.e., ∄ _C_<sup>_′_</sup> where _|C_<sup>_′_</sup> _| > |C|_ ). **MCP** for short. 

- **Maximum Independent Set (NP-hard)** : Select an independent set _S_ . Optimality requires identifying the maximum-size set of mutually non-adjacent nodes. **MIS** for short. 

15 

- **Minimum Vertex Cover (NP-hard)** : Determine a vertex cover _S_ . Optimal solution satisfies covering all edges with the minimum number of nodes. **MVC** for short. 

- **Maximum Common Subgraph (NP-hard)** : Identify the largest node-induced subgraph _S_ common to both _G_ and _H_ where edge relationships are preserved, with optimality determined by maximizing _|V_ ( _S_ ) _|_ . **MCS** for short. 

- **Graph Edit Distance (NP-hard)** : Calculate minimal edit operations (node/edge changes) to align _G_ with _H_ . Optimal solution minimizes total edit cost. **GED** for short. 

- **Traveling Salesman Problem (NP-hard)** : In a complete graph, find shortest Hamiltonian cycle. Optimal route minimizes<sup>�</sup> _w_ ( _ei_ ). **TSP** for short. 

In alignment with the original study’s framework, we maintain the original node range definitions across task categories: (1) Neighbor/Distance tasks operate with small graphs (4-19 nodes) and large graphs (2050 nodes); (2) Component/Diameter measurements alongside combinatorial problems (MCP/MIS/MVC) utilize small-scale graphs (4-14 nodes) contrasting with large-scale counterparts (15-30 nodes); (3) MCS/GED/TSP adhere to the established size parameters of small (4-9 nodes) versus large (10-20 nodes) instances. By employing the benchmark’s test datasets with unmodified size criteria, we preserve experimental continuity and facilitate meaningful cross-study comparisons. 

To address more general graph-theoretic challenges and facilitate algorithmic processing, we systematically convert the input representations of these tasks into a unified and structured schema. Detailed descriptions of the input structures and task specifications for each problem are documented in Appendix L. 

## **C License for GraphArena benchmark** 

We utilize the **GraphArena** benchmark to evaluate large language models on graph computational problems solely for academic research purposes. GraphArena is open-sourced under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license, as indicated in the official publication (Tang et al., 2025). 

The datasets incorporated within GraphArena originate from various sources, each with its respective licensing terms: 

- **DBLP** : CC0 1.0 Public Domain Dedication 

- **Social Network** : CC BY-SA 3.0 License 

- **DBpedia** : CC BY-SA 3.0 License 

- **OpenFlights** : Database Contents License (DbCL) v1.0 

- **PubChemQC (PCQM4Mv2)** : CC BY 4.0 License 

All datasets are publicly available and have been utilized in accordance with their respective licenses. The datasets employed, including those within the GraphArena benchmark, are either synthetic or derived from publicly available sources with appropriate anonymization measures in place. 

## **D Training and Inference Cost** 

We report below the training and inference costs for transparency: 

- **Training Cost** : The training process for the Llama-3-8B-Instruct model on the GraphThought dataset required approximately 138,828 seconds (38 hours) on a single NVIDIA H800 PCIe 80GB GPU. 

16 

- **Inference Cost** : The inference time per instance is approximately 0.0694 seconds for the Llama-38B-Instruct model and 0.0703 seconds for the fine-tuned model (Llama-GT). Notably, when using the fine-tuned model with Best-of-N (N=16), the inference time increases to approximately 0.1643 seconds per instance. This increase is not proportional to the number of queries (N=16) due to batch processing, which reduces computational overhead while generating more diverse responses to select the optimal answer. 

Table 3: Inference Time Cost of the Original Model, Llama-GT, and Llama-GT with Best-of-N (N=16) 

|**Model**|**Time (s)**|
|---|---|
|Llama-3-8B-Instruct|0.0694|
|Llama-GT|0.0703|
|Llama-GT (N=16)|0.1643|



## **E Complete Main Result with origin GraphArena results** 

17 

Table 4: Performance comparison of optimal solution rates (%) across 10 graph tasks, evaluated on small and large graphs, each has 500 instances. Results are shown for: (1) Original inference results of LLMs from GraphArena (Claude3-haiku, GPT-4o, etc.); (2) Code-augmented models (DeepSeek-V2-Coder, GPT-4o-Coder); (3)Supervised Fine-Tuned Model provided by GraphArena (Qwen2-7B-SFT);(4) Few-shot thought prompting variants (DeepseekV3, Llama-3.3-70B, etc.); (5) STaR framework implementations with different fewshot strategies; and (6) Our Llama-GT model trained with/without thought mechanisms. Metrics include polynomial tasks (Neighbor, Distance, Connected, Diameter), NP-hard tasks (MVC, MIS, MCP, TSP, MCS, GED).<sup>_∗_</sup> indicates that the model in the GraphArena paper was trained on fewer data compared to the data used in our model. 

||||Gra|ph Task (Sm|all Graphs)||||||
|---|---|---|---|---|---|---|---|---|---|---|
|Model|Neighbor|Distance|Connected|Diameter|MVC|MIS|MCP|TSP|MCS|GED|
|Claude3-haiku|0.768|0.580|0.260|0.116|0.336|0.450|0.482|0.242|0.282|0.216|
|DeepSeek-V2|0.540|0.814|0.474|0.226|0.376|0.360|0.400|0.368|0.236|0.282|
|Gemma-7b|0.410|0.496|0.014|0.086|0.128|0.212|0.254|0.134|0.020|0.028|
|gpt-3.5-turbo-0125|0.562|0.572|0.096|0.130|0.376|0.184|0.400|0.230|0.176|0.144|
|gpt-4o-2024-0513|0.860|0.796|0.794|0.426|0.326|0.518|0.528|0.404|0.406|0.268|
|Llama3-70b-Instruct|0.674|0.894|0.632|0.248|0.420|0.368|0.428|0.232|0.442|0.316|
|Llama3-8b-Instruct|0.368|0.412|0.248|0.114|0.318|0.282|0.280|0.162|0.096|0.072|
|Mixtral-8x7b|0.530|0.566|0.286|0.130|0.130|0.116|0.278|0.188|0.098|0.124|
|Qwen1.5-72b-Chat|0.572|0.478|0.394|0.118|0.224|0.386|0.388|0.228|0.298|0.174|
|Qwen1.5-8b-Chat|0.138|0.266|0.022|0.048|0.138|0.118|0.216|0.170|0.062|0.058|
|DeepSeek-V2-Coder|0.816|0.894|0.586|0.142|0.176|0.482|0.498|0.276|0.228|0.214|
|GPT-4o-Coder|0.808|0.654|0.712|0.334|0.296|0.530|0.644|**0.490**|0.508|0.320|
|Qwen2-7b-SFT<sup>_∗_</sup>|0.966|0.912|0.888|0.608|0.548|0.702|0.696|0.368|0.000|0.054|
|+Few-shot Thought|||||||||||
|Deepseek-V3|**1.000**|0.988|**1.000**|0.850|0.366|0.642|0.754|0.370|**0.544**|0.308|
|Llama-3.3-70B|0.970|0.970|0.954|0.674|0.206|0.648|0.554|0.292|0.484|0.326|
|Mixtral-8x7b|0.580|0.536|0.378|0.156|0.148|0.326|0.490|0.168|0.196|0.262|
|QwQ-32B-Preview|0.962|0.848|0.696|0.514|0.262|0.482|0.560|0.310|0.444|0.318|
|Llama3-8b-Instruct|0.700|0.480|0.502|0.070|0.108|0.248|0.258|0.190|0.222|0.450|
|+SFT|||||||||||
|STaR(w/ GT)|0.648|0.910|0.522|0.466|0.722|0.640|0.676|0.352|0.308|0.370|
|STaR(w/ LLM)|0.296|0.662|0.440|0.380|0.688|0.654|0.288|0.282|0.328|0.258|
|**Llama-GT(w/o Thought)**|0.988|0.990|0.906|0.820|0.930|0.972|0.906|0.366|0.538|**0.608**|
|**Llama-GT**|**1.000**|**1.000**|0.996|**0.954**|**0.972**|**0.994**|**0.952**|0.392|0.496|0.460|
||||Gra|ph Task (Lar|ge Graphs)||||||
|Model|Neighbor|Distance|Connected|Diameter|MVC|MIS|MCP|TSP|MCS|GED|
|Claude3-haiku|0.406|0.358|0.052|0.002|0.076|0.014|0.090|0.000|0.000|0.018|
|DeepSeek-V2|0.278|0.534|0.154|0.022|0.064|0.032|0.032|0.006|0.000|0.014|
|Gemma-7b|0.116|0.246|0.002|0.004|0.014|0.006|0.016|0.000|0.000|0.002|
|gpt-3.5-turbo-0125|0.412|0.322|0.012|0.008|0.082|0.008|0.052|0.000|0.000|0.006|
|gpt-4o-2024-0513|0.674|0.550|0.370|0.032|0.102|0.034|0.102|0.004|0.000|0.018|
|Llama3-70b-Instruct|0.434|0.530|0.264|0.034|0.114|0.026|0.106|0.000|0.000|0.008|
|Llama3-8b-Instruct|0.118|0.234|0.022|0.002|0.064|0.010|0.022|0.000|0.000|0.002|
|Mixtral-8x7b|0.232|0.282|0.040|0.000|0.036|0.008|0.034|0.000|0.000|0.006|
|Qwen1.5-72b-Chat|0.236|0.258|0.068|0.006|0.038|0.018|0.022|0.000|0.000|0.010|
|Qwen1.5-8b-Chat|0.026|0.156|0.002|0.000|0.002|0.000|0.016|0.000|0.000|0.006|
|DeepSeek-V2-Coder|0.672|0.632|0.206|0.008|0.080|0.028|0.072|0.000|0.022|0.014|
|GPT-4o-Coder|0.868|0.684|0.378|0.112|0.110|0.072|0.222|0.028|**0.036**|0.018|
|Qwen2-7b-SFT<sup>_∗_</sup>|0.790|0.570|0.230|0.092|0.156|0.054|0.136|0.000|0.000|0.032|
|+Few-shot Thought|||||||||||
|DeepSeek-V3|**0.992**|0.942|**0.932**|0.448|0.120|0.304|0.290|0.020|0.012|0.020|
|Llama-3.3-70B|0.952|0.866|0.856|0.290|0.118|0.254|0.136|0.000|0.012|0.012|
|Mixtral-8x7b|0.466|0.282|0.108|0.002|0.032|0.024|0.056|0.000|0.000|0.022|
|QwQ-32B-Preview|0.912|0.504|0.498|0.164|0.058|0.106|0.124|0.000|0.002|0.020|
|Llama3-8b-Instruct|0.604|0.220|0.132|0.002|0.028|0.010|0.038|0.000|0.002|0.026|
|+SFT|||||||||||
|STaR(w/ GT)|0.374|0.618|0.124|0.080|0.360|0.216|0.134|0.018|0.006|0.026|
|STaR(w/ LLM)|0.320|0.332|0.090|0.038|0.126|0.124|0.030|0.002|0.004|0.024|
|**Llama-GT(w/o Thought)**|0804|0864|0340|0302|0652|0652|0370|0024|0020|**0.068**|
|<br>**Llama-GT**|.<br>0.988|.<br>**0.984**|.<br>0.836|.<br>**0.600**|.<br>**0.744**|.<br>**0.900**|.<br>**0.634**|.<br>**0.036**|.<br>**0.036**|0.008|



18 

## **F Methods for constructing action thoughts and state thoughts for GCO problem** 

### **F.1 Action thoughts generation methods** 

For a GCO problem, there are mainly three classes of methods to construct action thought set _A_ with heuristics. 

- **Ordinary Generation Rule** : Foundational strategies (e.g., greedy selection, random sampling) provide baseline mechanisms for generating thoughts. These rule-based approaches offer broad applicability across diverse problem domains through their simplicity. 

- **Simple Heuristic Thoughts:** Heuristics of GCO problems leverage structural properties of target 

- problems to enhance operational efficiency. Such methods typically derive from simple reasoning conclusions of the problem. 

- **Complex Heuristic Thoughts:** Complex heuristics involve a broader set of operational primitives, 

- presenting two fundamental challenges. First, their intricate implementation mechanisms lack intuitive interpretability. Second, the expanded solution space necessitates consideration of diverse operational combinations. These characteristics hinder LLMs from effectively discerning the underlying principles learning such heuristics. 

- **Mixed Heuristic Thoughts:** The former strategies possess distinct advantages, hybrid approaches 

- demonstrate superior efficacy in specific problem contexts through strategic combination of complementary strategies. 

### **F.2 State thoughts generation methods** 

In solving a GCO problem, maintaining instance state descriptions is essential for two reasons. First, the GCO instance evolves with each reasoning step, requiring the removal of redundant elements. Second, explicitly tracking instance states prevents hallucinations in LLMs. The following state thought generation methods are defined. 

- **Instance Description:** Recording the current GCO instance information forms the foundational state representation. For example describe the node set _V_ and edge set _E_ of a graph _G_ . 

- **Instance Simplification:** Pruning redundant elements after every reasoning step. For example, in 

- maximum independent set (MIS) problems, removing all neighbors of the current MIS set from the graph _G_ . 

- **Instance Reduction:** Transforming instances into equivalent problem spaces. For instance, solving MIS of _G_ can be reduced to finding minimum vertex cover (MVC) of _G_ ’s complement graph _G_<sup>¯</sup> . 

- **Solution Description:** The solution information not only emphasizes the importance of the solution but also shows the changes of the solution. This prompts the LLM to explicitly track how selected actions influence the current solution. 

- **Solving flag:** Formal stopping criteria marking solution completion through state indicators. 

## **G Usual action thoughts and state thoughts for GCO problem** 

In graph optimization problems, the fundamental heuristic operations primarily comprise four canonical primitives: node addition, node deletion, edge addition, and edge deletion. Formally, let A denote the action thought space for graph optimization, which includes the following important actions: 

- Add Nodes Based on the Given Optimal Solution ( _a_ 1): Add one or more nodes to the current solution set based on the given optimal solution. 

- Add Nodes Based on Rules ( _a_ 2): Add one or more nodes to the current solution set using rules such as greedy or random selection. 

- Add Nodes Based on Simple Prior Knowledge ( _a_ 3): Add one or more nodes to the current solution set using simple prior knowledge. 

- Add Nodes Based on Complex Prior Knowledge ( _a_ 4): Add one or more nodes to the current solution set using complex prior knowledge. 

19 

- Remove Nodes Based on the Given Optimal Solution ( _a_ 5): Remove one or more nodes from the current solution set based on the given optimal solution. 

- Remove Nodes Based on Rules ( _a_ 6): Remove one or more nodes from the current solution set using rules such as greedy or random selection. 

- Remove Nodes Based on Simple Prior Knowledge ( _a_ 7): Remove one or more nodes from the current solution set using simple prior knowledge. 

- Remove Nodes Based on Complex Prior Knowledge ( _a_ 8): Remove one or more nodes from the current solution set using complex prior knowledge. 

- Add Edges Based on the Given Optimal Solution ( _a_ 9): Add one or more edges to the current solution set based on the given optimal solution. 

- Add Edges Based on Rules ( _a_ 10): Add one or more edges to the current solution set using rules such as greedy or random selection. 

- Add Edges Based on Simple Prior Knowledge ( _a_ 11): Add one or more edges to the current solution set using simple prior knowledge. 

- Add Edges Based on Complex Prior Knowledge ( _a_ 12): Add one or more edges to the current solution set using complex prior knowledge. 

- Remove Edges Based on the Given Optimal Solution ( _a_ 13): Remove one or more edges from the current solution set based on the given optimal solution. 

- Remove Edges Based on Rules ( _a_ 14): Remove one or more edges from the current solution set using rules such as greedy or random selection. 

- Remove Edges Based on Simple Prior Knowledge ( _a_ 15): Remove one or more edges from the current solution set using simple prior knowledge. 

- Remove Edges Based on Complex Prior Knowledge ( _a_ 16): Remove one or more edges from the current solution set using complex prior knowledge. 

The fundamental state thought space S for graph optimization problems is defined through node and edge set representations. Formally, the main canonical state components are structured as follows: 

- Solving State ( _s_ 1): Describes the solving state to determine whether the process is complete. 

- Add Nodes to the Graph ( _s_ 2): Describes the operation of adding nodes to the original graph for subsequent solving. 

- Remove Nodes from the Graph ( _s_ 3): Describes the operation of removing nodes from the original graph for subsequent solving. 

- Add Edges to the Graph ( _s_ 4): Describes the operation of adding edges to the original graph for subsequent solving. 

- Remove Edges from the Graph ( _s_ 5): Describes the operation of removing edges from the original graph for subsequent solving. 

- Graph Node Set ( _s_ 6): Describes the set of all nodes or partial nodes in the original graph. 

- Graph Edge Set ( _s_ 7): Describes the set of all edges or partial edges in the original graph. 

- Current Solution Set ( _s_ 8): Describes the set of elements in the current solution. 

- Final Solution Set ( _s_ 9): Describes the set of elements in the final solution. 

20 

## **H Concrete Applications of Forward and Backward MTP Frameworks** 

### **H.1 A Forward MTP for the Connected Components Problem** 

**Algorithm 2** A Thoughts Template for Connected Component Problem 

- **Require:** Graph _G_ = ( _V, E_ ) 1: _CC ←∅_ ; _▷_ Initialize connected components 2: **while** _V̸_ = _∅_ **do** 3: Action: choose a node for BFS randomly; 4: _u ←_ RandomSelect( _G_ ); _▷_ Random node selection 5: _Cu ←_ BFS( _G, u_ ); _▷_ Component discovery 6: _CC ← CC ∪{Cu}_ ; 7: _V ← V \ Cu_ ; _▷_ Graph simplification 

- 8: **end while** 

- 9: State: describe connected components in _CC_ ; 

- 10: **return** _CC_ ; 

- **Algorithm 3** Breadth-First Search( _G_ , _u_ <u>)</u> **Require:** Graph _G_ , start node _u_ **Ensure:** Connected component _C_ 1: Action: Start BFS at node _u_ of _G_ ; 2: _L ←{u}_ ; _▷_ Nodes waiting to be visited 3: _C ←∅_ ; _▷_ Visited nodes 4: **while** _L̸_ = _∅_ **do** 5: _v ←_ PopFrom(L); _▷_ Select unvisited node 6: Action: add _v_ to the current component; 7: _C ← C ∪{v}_ ; 8: **for** _w ∈_ Neighbor( _G_ , _v_ ) **do** 9: **if** _w ∈/ C ∧ w ∈/ L_ **then** 

- 10: AddTo( _w, L_ ); _▷_ Record unvisited nodes 11: State: add an unvisited neighbor _w_ to _L_ ; 12: **end if** 

- 13: **end for** 14: State: show the current visited nodes _C_ ; 

15: **end while** 16: State: finished, show the connected component _C_ ; 17: **return** _C_ ; 

The Connected Components (CC) problem requires identifying all maximally connected subgraphs in an undirected graph _G_ . Formally, given _G_ = ( _V, E_ ), the goal is to partition _V_ into disjoint subsets _{C_ 1 _, . . . , Ck}_ where each _Ci_ forms a connected subgraph. **Action Thought Generation Methods:** 

- **A simple heuristic thought: Breadth-First Search (BFS)** , systematically explores node neighborhoods through queue-based traversal (lines 1 and 6 of Algorithm 3). 

- **An ordinary generation rule: Random Selection** , chooses initial nodes for BFS through random sampling (line 3 of Algorithm 2 ). 

These action thoughts in the three lines constitute the set _A_ . **State Thought Generation Methods:** 

21 

- **Instance Simplification** : Add an unvisited node to the queue of nodes to be visited (line 11 of Algorithm 3). 

- **Solution Description** : Current connected component being explored (line 14 of Algorithm 3, line 9 of Algorithm 2). 

- **Solving Flag** : Indicator for algorithm completion (line 16 of Algorithm 3 ). 

These state thoughts in the four lines constitute the set _S_ . 

A forward MTP for CC is shown in Algorithm 2. RandomSelect( _G_ ) select randomly a node _u_ of _G_ . In BFS, the queue _L_ stores nodes awaiting visitation, while set _C_ maintains all visited nodes. When _L̸_ = _∅_ , the algorithm selects a node _v_ of _L_ to visit, then adds _v_ ’s unvisited neighbors to _L_ . PopFrom(L) pops the first node of _L_ . Neighbor( _G_ , _v_ ) returns all neighbor node of _v_ in _G_ . AddTo( _w_ , _L_ ) appends _w_ to the end of _L_ . 

### **H.2 A Backward MTP for the MIS Problem** 

**Algorithm 4** A Thought Template for MIS 

**Require:** Graph _G_ = ( _V, E_ ), a mis solver _X_ . 1: _OPT ←X_ ( _G_ ); _▷_ Compute optimal MIS 2: _MIS ←∅_ ; _▷_ Initialize solution 3: **while** _V̸_ = _∅_ **do** 4: Action: add all isolated nodes to _MIS_ ; 5: _MIS ← MIS ∪_ Isolated( _G_ ); _▷_ Add all isolated nodes 6: Action: add one node of _OPT_ to _MIS_ ; 7: _u ←_ AddOne( _OPT_ ); _▷_ Add optimal node 8: _MIS ← MIS ∪{u}_ ; 9: State: describe the current _MIS_ ; 10: State: delete all neighbors of _u_ in G; 11: _V ← V \_ (Isolated( _G_ ) _∪_ Neighbor( _G, u_ ) _∪{u}_ ); _▷_ Remove useless nodes 12: _OPT ← OPT \ MIS_ ; 13: State: describe the current _G_ ; 14: **end while** 15: State: finished, describe the solution _MIS_ ; 16: **return** _MIS_ . 

The MIS problem identifies the largest subset of non-adjacent nodes. The AddOne thought comprises two specialized operations: 

- **AddOne: Add Isolated Nodes** , immediately incorporates all isolated nodes into the current solution _MIS_ (line 4 of Algorithm 4). 

- **AddOne: Add Optimal Nodes** , selectively integrates one node from solver outputs into the current solution _MIS_ (line 6 of Algorithm 4). 

The first action atomically adds all isolated nodes to the current solution because all isolated nodes belong to the optimal MIS solution. These action thoughts in the two lines constitute the set _A_ . **State Thought Generation Methods:** 

- **Instance Description** : Maintains graph _G_ ’s current structure (line 13 of Algorithm 4) 

- **Instance Simplification** : Records graph simplification operations (line 10 of Algorithm 4) 

- **Solution Description** : Tracks current/final solution candidates (lines 9 & 15 of Algorithm 4) 

- **Solving Flag** : Monitors termination conditions (line 15 of Algorithm 4) 

22 

These state thoughts in the four lines constitute the set _S_ . 

A backward MTP for MIS is shown as follows. An integer programming model of MIS problem is put into Gurobi, which serves as an optimal solution solver. Isolated( _G_ ) returns all nodes of _G_ without neighbors. 

## **I Ablation and Supplementary Experiments** 

### **I.1 Impact of Thought Types: State vs Action** 

We conducted a focused ablation to understand the role of state vs. action thoughts. The results show that use only action thoughts yields worse performance than even the no-thought baseline, suggesting that action thoughts alone lead to unstructured, less interpretable reasoning chains. The integration of state thoughts plays a crucial role in structuring the reasoning process, enabling more effective optimization. 

Table 5: Ablation: Effect of Thought Types 

|Method|Polynomial Task|NP-Hard Task|
|---|---|---|
|Llama3-8B (w/o thoughts)|0.752|0.509|
|Llama3-8B (action-only)|0.741|0.488|
|Llama3-8B (full thoughts)|**0.920**|**0.552**|



### **I.2 Comparison with Classical Heuristics on MIS** 

We benchmarked Llama-GT against classical baselines including Greedy, Luby’s Algorithm(Luby, 1986), and BDOne(Chang et al., 2017). As the Best-of-N (BoN) value increases, Llama-GT demonstrates significant performance improvements. On both easy and hard instances, Llama-GT with higher BoN values not only surpasses heuristic approaches but also achieves performance comparable to the Gurobi solver, particularly excelling in high-difficulty settings. 

Table 6: Comparison on MIS Problem (Average Solution Size) 

|Method|MIS_easy|MIS_hard|
|---|---|---|
|Llama-GT (N=1)|4.472|11.844|
|Llama-GT (N=16)|4.502|12.568|
|Llama-GT (N=32)|4.502|**12.570**|
|Greedy|4.502|12.562|
|Luby|4.502|12.568|
|BDOne|4.502|12.568|
|Gurobi|4.502|**12.570**|



### **I.3 Relative Improvements Across Different Model Scales** 

Table 7: Performance Across Model Scales, *inf means the pre-finetuning result is 0.0 

|**Task**|**Llama3.2-3B**<sup>11</sup>|**Llama3-8B**|
|---|---|---|
|MIS|0.988 (+766.7%)|0.994 (+300.8%)|
|Diameter|0.872 (+2625.0%)|0.954 (+1262.9%)|
|MCS|0.394 (+310.4%)|0.496 (+123.4%)|
|MIS (Hard)|0.870 (+21650.0%)|0.900 (+8900.0%)|
|Diameter (Hard)|0.358 (inf)|0.600 (+29900.0%)|
|MCS (Hard)|0.018 (inf)|0.036 (+1700.0%)|



23 

Due to computational constraints, we could not fine-tune the Llama3-70B model, but instead evaluated generalization trends using smaller-scale models. Our analysis reveals that the relative performance gain from thought integration diminishes with increasing model size, suggesting that larger models inherently possess stronger reasoning capabilities. Nevertheless, thought guidance remains valuable—it significantly enhances the capabilities of smaller models, potentially providing a more computationally efficient alternative to pure model scaling. We recommend that future research investigate this hypothesis across a broader range of model sizes to better understand the scaling dynamics. 

## **J Performance Degradation on Certain NP-hard Problems** 

While our method demonstrates strong performance on specific NP-hard tasks such as MIS, achieving significant improvements over baseline models, we observe relatively modest gains for tasks like TSP, MCS, and GED. In certain instances, performance metrics even regressed below those of baseline models trained without thought mechanisms, particularly for the GED task. 

We posit two principal factors contributing to this performance disparity: 

First, these tasks inherently exhibit **higher computational complexity** compared to problems like MIS or MCP, presenting greater challenges for LLM-based solutions. 

Second, the thought construction process for TSP, MCS, and GED primarily utilizes a single action type (e.g., “Add Nodes Based on the Given Optimal Solution,” detailed in Appendix G). This monolithic approach operates as a **black-box mechanism** , limiting the incorporation of domain-specific prior knowledge or structural knowledge. Conversely, tasks like MIS benefit from diverse action types (e.g., both “Add Nodes Based on the Given Optimal Solution” and “Add Nodes Based on Simple Prior Knowledge”) and state transformations (e.g., “Remove Nodes from the Graph”). These mechanisms effectively **embed structural priors** (e.g., mandatory inclusion of isolated nodes in independent sets) and **systematically prune the search space** , thereby reducing hallucination risks while enhancing solution quality. For detailed thought construction examples, please refer to Appendix L. 

## **K Automated Thought Dataset Synthesis via LLM-Driven Code Generation** 

We created a template to automate dataset generation for ten tasks using a LLM(Qwen2.5-Coder-32BInstruct<sup>12</sup> ). This automated approach generated valid code for the tasks, creating datasets of equivalent size to fine-tune the Meta-Llama-3-8B-Instruct model. We compared four configurations: 1) Origin: The base model, 2) w/o Thought: Fine-tuned with direct-answer supervision, 3) Llama-GT (w/ LLM-Design): Fine-tuned on datasets generated by LLM-synthesized code, and 4) Llama-GT (w/ Human-Design): Fine-tuned on datasets generated by human-designed code. 

As shown in Figure 5, Llama-GT (w/ LLM-Design) significantly improves reasoning capabilities over the Origin model, outperforming w/o Thought on Polynomial tasks. However, on NP-hard tasks, the LLM-generated code struggles to produce high-quality thought sequences, resulting in performance similar to w/o Thought (0 _._ 509 vs. 0 _._ 508). While Llama-GT (w/LLM-Design) lags behind Llama-GT (w/Human-Design) in both categories, it offers advantages like lower construction costs for unseen problems and better compatibility with optimization methods. Future work will focus on developing frameworks to improve the quality and generality of LLM-generated datasets. 

> 12https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct 

24 



Figure 5: Performance comparison of Meta-Llama-3-8B-Instruct variants on Polynomial and NP-hard tasks: Base model (Origin), fine-tuned with direct-answer datasets (w/o Thought),datasets generated using LLM-synthesized code Llama-GT (w/LLM-Design), and datasets generated using human-designed code Llama-GT (w/HumanDesign). The values represent the average ratio of the number of optimal solutions achieved across different tasks. 

### **K.1 Automated Thought Dataset Generation Template** 

### **K.1.1 Outer Prompt** 

- <mark>You are a professional mathematician and computer scientist. I am working on solving a graph theory problem called {TASK NAME}. {TASK DESCRIPTON} I want to</mark> 

- <mark>reconstruct the steps involved in solving this graph theory problem starting from the optimal solution. Please help me construct a subset of combinations of states and actions from the following state thought space and action thought space , so that the algorithm using this subset can clearly and step -by -step output the optimal reasoning process for solving {task.task_full_name} in textual form. Please do not use any third -party libraries or known algorithms to simply obtain the final answer. What we need is the reasoning process for</mark> 

- <mark>solving the problem in as much detail as possible.</mark> 

- <mark>The states describe the transformations and intermediate stages of the graph during the solution process. Each element in the state thought space is defined and explained as follows:</mark> 

- <mark>1. Solving State: Describes the solving state to determine whether the process is complete.</mark> 

- <mark>2. Add Nodes to the Graph: Describes the operation of adding nodes to the original graph for subsequent solving.</mark> 

- <mark>3. Remove Nodes from the Graph: Describes the operation of removing nodes from the original graph for subsequent solving.</mark> 

- <mark>4. Add Edges to the Graph: Describes the operation of adding edges to the original graph for subsequent solving.</mark> 

<mark>5. Remove Edges from the Graph: Describes the operation of removing edges from the original graph for subsequent solving.</mark> 

<mark>6. Graph Node Set: Describes the set of all nodes or partial nodes in the original graph.</mark> 

<mark>7. Graph Edge Set: Describes the set of all edges or partial edges in the original graph.</mark> 

<mark>8. Current Solution Set: Describes the set of elements in the current solution.</mark> 

<mark>9. Final Solution Set: Describes the set of elements in the final solution.</mark> 

- <mark>The actions represent operations performed on the solution set. Each element in the action thought space is defined and explained as follows:</mark> 

<mark>1. Add Nodes Based on the Given Optimal Solution: Add one or more nodes to the current solution set based on the given optimal solution.</mark> 

25 

<mark>2. Add Nodes Based on Rules: Add one or more nodes to the current solution set using rules such as greedy or random selection.</mark> 

<mark>3. Add Nodes Based on Simple Prior Knowledge: Add one or more nodes to the current solution set using simple prior knowledge.</mark> 

<mark>4. Add Nodes Based on Complex Prior Knowledge: Add one or more nodes to the current solution set using complex prior knowledge.</mark> 

<mark>5. Remove Nodes Based on the Given Optimal Solution: Remove one or more nodes from the current solution set based on the given optimal solution.</mark> 

<mark>6. Remove Nodes Based on Rules: Remove one or more nodes from the current solution set using rules such as greedy or random selection.</mark> 

<mark>7. Remove Nodes Based on Simple Prior Knowledge: Remove one or more nodes from the current solution set using simple prior knowledge.</mark> 

<mark>8. Remove Nodes Based on Complex Prior Knowledge: Remove one or more nodes from the current solution set using complex prior knowledge.</mark> 

<mark>9. Add Edges Based on the Given Optimal Solution: Add one or more edges to the current solution set based on the given optimal solution.</mark> 

<mark>10. Add Edges Based on Rules: Add one or more edges to the current solution set using rules such as greedy or random selection.</mark> 

<mark>11. Add Edges Based on Simple Prior Knowledge: Add one or more edges to the current solution set using simple prior knowledge.</mark> 

<mark>12. Add Edges Based on Complex Prior Knowledge: Add one or more edges to the current solution set using complex prior knowledge.</mark> 

<mark>13. Remove Edges Based on the Given Optimal Solution: Remove one or more edges from the current solution set based on the given optimal solution.</mark> 

<mark>14. Remove Edges Based on Rules: Remove one or more edges from the current solution set using rules such as greedy or random selection.</mark> 

<mark>15. Remove Edges Based on Simple Prior Knowledge: Remove one or more edges from the current solution set using simple prior knowledge.</mark> 

<mark>16. Remove Edges Based on Complex Prior Knowledge: Remove one or more edges from the current solution set using complex prior knowledge.</mark> 

<mark>Here , I'll give you two examples about what to output: Example 1: {</mark> 

- <mark>"input ": "In an undirected graph , (i,j) means that node i and node j are connected with an undirected edge. I'll give an instance of a graph , please help me find the maximum independent set in the graph and list the steps and results for each iteration. The Maximum Independent Set problem is an optimization</mark> 

- <mark>problem in graph theory that aims to identify the largest set of vertices in a graph , where no two vertices in the set are adjacent ."</mark> 

- <mark>"output ": {" Solving State": "Determine whether the current graph is an empty graph.", "Add Nodes Based on Simple Prior Knowledge ": "Add isolated nodes: [].", "Add Nodes Based on the Given Optimal Solution ": "Add the most appropriate node</mark> 

- <mark>: [].", "Remove Nodes from the Graph ": "Remove the neighboring nodes of the node : [].", "Graph Node Set": "The remaining nodes of the graph are: [].", "Current Solution Set": "The current Independent Set is: [].", "Final Solution Set": "The maximum independent set is []."}</mark> 

<mark>} Example 2: {</mark> 

- <mark>"input ": "In an undirected graph , (i,j) means that node i and node j are connected with an undirected edge. I'll give an instance of a graph and two nodes , please help me find the common neighbor nodes of the given two nodes in the graph."</mark> 

- <mark>"output ": {"Graph Node Set": "The neighboring nodes of the node <chosen node 1>: [].", "Graph Node Set": "The neighboring nodes of the node <chosen node 2>:</mark> 

- <mark>[].", "Final Solution Set": "The common neighbor nodes of the two nodes are: []."}</mark> 

<mark>}</mark> 

- <mark>Please provide the state and action combinations along with their descriptions for { TASK NAME} based on the format of "output" above. {TASK DESCRIPTION} Do not provide any explanations or descriptions related to "output" and there is no need to provide any examples. Since the nodes and edges of the original graph will be provided in the input , in order to keep the output inference text brief , please avoid choosing Graph Node Set and Graph Edge Set to describe the</mark> 

- <mark>original graph unless necessary.</mark> 

### **K.1.2 Inner Prompt** 

26 

<mark>You are a professional mathematician and computer science expert. I am working on solving a graph theory problem called {task.task_full_name }. {task. task_description ()} I would like to reconstruct the steps involved in solving this graph theory problem starting from the optimal solution. Please help me build a Python function using all the provided combinations of states and actions , so that this function can return the reasoning steps to solve the problem. Please do not use any third -party libraries or known algorithms to simply obtain the final answer. What we need is the reasoning process for solving the problem in as much detail as possible. Here is two examples: Example 1: {</mark> 

<mark>"input ": "In an undirected graph , (i,j) means that node i and node j are connected with an undirected edge. I'll give an instance of a graph , please help me find the maximum independent set in the graph and list the steps and results for each iteration. The Maximum Independent Set problem is an optimization problem in graph theory that aims to identify the largest set of vertices in a graph , where no two vertices in the set are adjacent. Here 's the combination of states and actions constructed from expert: {{" Solving State ": "Determine whether the current graph is an empty graph.", "Add Nodes Based on Simple Prior Knowledge ": "Add isolated nodes: [].", "Add Nodes Based on the Given Optimal Solution ": "Add the most appropriate node: [].", "Remove Nodes from the Graph ": "Remove the neighboring nodes of the node: [].", "Graph Node Set": "The remaining nodes of the graph are: [].", "Current Solution Set": "The current Independent Set is: [].", "Final Solution Set": "The maximum independent set is []."}}" "output ":</mark> ````` <mark>python def mis_optimal_trace(G_: nx.Graph , optimal_solution: List[int]) -> Tuple[str , List[ int ]]: G = G_.copy() s = "" mis = optimal_solution.copy() I = [] while G: # Solving State Isopnts = [u for u in G if len(list(G.neighbors(u))) == 0] I.extend(Isopnts) s += f"Add isolated nodes: {{list(set(Isopnts))}}.\\n" # Add Nodes Based on Simple Prior Knowledge G.remove_nodes_from(Isopnts) if not G: s += f"The remaining nodes of the graph are: {{list(G.nodes)}}.\\n" # Graph Node Set break</mark> 

<mark>mis = [elem for elem in mis if elem not in I] chosen_node = random.choice(mis) I.append(chosen_node) s += f"Add the most appropriate node: {{ chosen_node }}.\\n" # Add Nodes Based on the Given Optimal Solution</mark> 

<mark>s += f"Remove the neighboring nodes of the node {{ chosen_node }}: {{list(G. neighbors(chosen_node))}}.\\n" # Remove Nodes from the Graph</mark> 

<mark>G.remove_nodes_from(list(G.neighbors(chosen_node))) G.remove_node(chosen_node) s += f"The remaining nodes of the graph are: {{list(G.nodes)}}.\\n" # Graph Node Set s += f"The current Independent Set is: {{I}}.\\n" # Current Solution Set s += "Finished !\\n" s += f'The maximum independent set is {{mis}}.' # Final Solution Set return s, I</mark> 

````` <mark>} Example 2: { "input ": "In an undirected graph , (i,j) means that node i and node j are connected with an undirected edge. I'll give an instance of a graph and two nodes , please help me find the common neighbor nodes of the given two nodes in the graph. Here 's the combination of states and actions constructed from expert: {{" Graph Node Set": "The neighboring nodes of the node <chosen node 1>: [].", "Graph Node Set": "The neighboring nodes of the node <chosen node 2>: [].", "Final Solution</mark> 

27 

<mark>Set": "The common neighbor nodes of the two nodes are: []."}}" "output ":</mark> ````` <mark>python def neighbor_optimal_trace(G_: nx.Graph , chosen_nodes: List[int], optimal_solution: List[int]) -> Tuple[str , List[int ]]: G = G_.copy() s = "" neighbor_node_1 = list(G.neighbors(chosen_nodes [0])) neighbor_node_2 = list(G.neighbors(chosen_nodes [1])) common_neighbor_nodes = list(set(neighbor_node_1) & set(neighbor_node_2)) s += f"The neighboring nodes of the node {{ chosen_nodes [0]}}: {{ neighbor_node_1 }}.\\n" # Graph Node Set s += f"The neighboring nodes of the node {{ chosen_nodes [1]}}: {{ neighbor_node_2 }}.\\n" # Graph Node Set s += f"The common neighbor nodes of the two nodes are: {{ common_neighbor_nodes }}.\\n" # Final Solution Set return s, common_neighbor_nodes</mark> ````` <mark>} Here 's the input: "{TASK DESCRIPTION} Here 's the combination of states and actions constructed from expert: {OUTER RESPONSE }."</mark> 

- <mark>Please provide the python code of solution for {TASK NAME} based on the format of " output" above. Do not provide any explanations or descriptions related to " output ," and there is no need to provide any examples. Please use all the provided states and actions set to construct the function. Here 's the function definition header: "{TASK FUNCTION HEADER }". Please construct the optimal Python code to solve the problem. Ensure the code is correct , the reasoning steps are</mark> 

- <mark>complete , and the code is highly readable , while minimizing the length of the reasoning text as much as possible. And you must concatenate '{TASK OUTPUT FORMAT}' at the end of your code , where <final answer > is a python list. Do not modify , add , or delete any words or symbols in the statement , and do not change case.</mark> 

### **K.1.3 Example** 

Here, we use the Minimum Vertex Cover problem as an example to demonstrate the Outer output and Inner output generated using the above-mentioned template. The problem description is as follows. 

- <mark>In an undirected graph , (i,j) means that node i and node j are connected with an undirected edge. I'll give an instance of a graph , please help me find the minimum vertex cover in the graph and list the steps and results for each iteration. The Minimum Vertex Cover problem is an optimization problem in graph theory that aims to find the smallest set of vertices in a graph such that every edge in the graph is incident to at least one vertex in the set.</mark> 

### **Outer Output** 

- <mark>{'Solving State ': 'Determine whether the current graph is an empty graph.', 'Add Nodes Based on Simple Prior Knowledge ': 'Add nodes with the highest degree: [].', 'Add Nodes Based on the Given Optimal Solution ': 'Add the most appropriate node: [].', 'Remove Nodes from the Graph ': 'Remove the selected node and its</mark> 

- <mark>incident edges: [].', 'Graph Node Set ': 'The remaining nodes of the graph are: [].', 'Graph Edge Set ': 'The remaining edges of the graph are: [].', 'Current Solution Set ': 'The current Vertex Cover is: [].', 'Final Solution Set ': 'The minimum vertex cover is [].'}</mark> 

### **Inner Output** 

<mark>def mvc_optimal_trace(G_: nx.Graph , optimal_solution: List[int]) -> str: G = G_.copy() s = "" mvc = optimal_solution.copy() C = [] while G: # Solving State if not G.edges: s += "The graph is empty .\n" break</mark> 

<mark># Add Nodes Based on Simple Prior Knowledge degrees = dict(G.degree ())</mark> 

28 

<mark>max_degree_node = max(degrees , key=degrees.get) C.append(max_degree_node) s += f"Add nodes with the highest degree: {max_degree_node }.\n" # Remove Nodes from the Graph neighbors = list(G.neighbors(max_degree_node)) G.remove_node(max_degree_node) s += f"Remove the selected node and its incident edges: {max_degree_node }.\n " # Graph Node Set and Edge Set s += f"The remaining nodes of the graph are: {list(G.nodes)}.\n" s += f"The remaining edges of the graph are: {list(G.edges)}.\n" # Current Solution Set s += f"The current Vertex Cover is: {C}.\n" s += "Finished !\n" s += f'The minimum vertex cover is {mvc}.' # Final Solution Set return s</mark> 

## **L Detailed Case Studies of Thought Processes** 

In this section, we present ten concrete task examples accompanied by their corresponding reasoning thoughts to systematically demonstrate the thought construction methodology. 

Table 8: An example of the Connected Component task. 

**Task Description** In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, and the task is to identify one representative node from each connected component within the graph. 

**Input** 

The graph has 7 nodes. The nodes are numbered from 0 to 6, and the edges are: [(0, 3), (2, 6), (3, 4), (4, 6)]. 

**Output** Choose node 0 as the start point of the current connectivity component. Add node 0 into the connected component list. Add the unvisited neighboring nodes of the node 0 into the search queue: [3]. Add node 3 into the connected component list. Add the unvisited neighboring nodes of the node 3 into the search queue: [4]. Add node 4 into the connected component list. Add the unvisited neighboring nodes of the node 4 into the search queue: [6]. The current connected component is: [0, 3, 4]. Add node 6 into the connected component list. Add the unvisited neighboring nodes of the node 6 into the search queue: [2]. Add node 2 into the connected component list. Add the unvisited neighboring nodes of the node 2 into the search queue: []. Finished! Connected component 1: Nodes = [0, 3, 4, 6, 2], Representative node = 0. Choose node 1 as the start point of the current connectivity component. Add node 1 into the connected component list. Add the unvisited neighboring nodes of the node 1 into the search queue: []. Finished! Connected component 2: Nodes = [1], Representative node = 1. Choose node 5 as the start point of the current connectivity component. Add node 5 into the connected component list. Add the unvisited neighboring nodes of the node 5 into the search queue: []. Finished! Connected component 3: Nodes = [5], Representative node = 5. The representative nodes for each connected component are: [0, 1, 5]. 

29 

Table 9: An example of the Shortest Distance task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, please help me find the shortest path between two nodes in the graph and list the steps and results for each iteration. The shortest path between two nodes is defined as the path with the fewest edges that connect the source node to the target node. If no path exists, output an empty path. 

##### **Input** 

The graph has 9 nodes. The nodes are numbered from 0 to 8, and the edges are: [(0, 7), (0, 8), (1, 3), (1, 8), (2, 6), (3, 6), (4, 8), (6, 7), (7, 8)]. The source node is 4, and the target node is 3. 

**Output** Current path: [4], the neighboring nodes of the node 4: [8]. Current path: [4, 8], the neighboring nodes of the node 8: [0, 1, 4, 7]. Current path: [4, 8, 0], the neighboring nodes of the node 0: [7, 8]. Current path: [4, 8, 1], the neighboring nodes of the node 1: [3, 8]. Found the target node 3. The shortest path is [4, 8, 1, 3]. 

Table 10: An example of the Common Neighbor task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph and two nodes, please help me find the common neighbor nodes of the given two nodes in the graph. 

##### **Input** 

The graph has 10 nodes. The nodes are numbered from 0 to 9, and the edges are: [(0, 1), (0, 3), (0, 5), (0, 7), (0, 8), (1, 3), (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 4), (2, 7), (2, 8), (2, 9), (3, 5), (3, 6), (3, 7), (3, 9), (4, 7), (4, 9), (5, 6), (5, 8), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)]. The given nodes are [7, 3]. 

##### **Output** 

The neighboring nodes of the node 7: [0, 1, 2, 3, 4, 8, 9]. The neighboring nodes of the node 3: [0, 1, 2, 5, 6, 7, 9]. The common neighbor nodes of the two nodes are: [0, 1, 2, 9]. 

Table 11: An example of the Minimum Vertex Cover task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, please help me find the minimum vertex cover in the graph and list the steps and results for each iteration. The Minimum Vertex Cover problem is an optimization problem in graph theory that aims to find the smallest set of vertices in a graph such that every edge in the graph is incident to at least one vertex in the set. 

##### **Input** 

The graph has 10 nodes. The nodes are numbered from 0 to 9, and the edges are: [(1, 5), (1, 6), (2, 7)]. 

##### **Output** 

Remove isolated nodes: [0, 3, 4, 8, 9]. Add the most appropriate node: 1. The current Vertex Cover is: [1]. Remove the edges of node 1: [(1, 5), (1, 6)]. Remove isolated nodes: [1, 5, 6]. Add the most appropriate node: 2. The current Vertex Cover is: [1, 2]. Remove the edges of node 2: [(2, 7)]. Remove isolated nodes: [2, 7]. There is no edge left in the graph. Finished! The minimum vertex cover is [1, 2]. 

30 

#### Table 12: An example of the Maximum Independent Set task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, please help me find the maximum independent set in the graph and list the steps and results for each iteration. The Maximum Independent Set problem is an optimization problem in graph theory that aims to identify the largest set of vertices in a graph, where no two vertices in the set are adjacent. 

##### **Input** 

The graph has 8 nodes. The nodes are numbered from 0 to 7, and the edges are: [(3, 4), (5, 6)]. 

##### **Output** 

Add isolated nodes: [0, 1, 2, 7]. Add the most appropriate node: 3. The current Independent Set is: [0, 1, 2, 7, 3]. Remove the neighboring nodes of the node 3: [4]. The remaining nodes of the graph are: [5, 6]. Add isolated nodes: []. Add the most appropriate node: 5. The current Independent Set is: [0, 1, 2, 7, 3, 5]. Remove the neighboring nodes of the node 5: [6]. The remaining nodes of the graph are: []. Finished! The maximum independent set is [0, 1, 2, 7, 3, 5]. 

#### Table 13: An example of the Graph Diameter task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, please help me find the diameter of the graph and list the steps and results for each iteration. The diameter of a graph is the longest shortest path between any two nodes in the graph. 

##### **Input** 

The graph has 10 nodes. The nodes are numbered from 0 to 9, and the edges are: [(0, 1), (0, 9), (1, 3), (2, 3), (3, 4), (3, 6), (4, 6), (5, 9), (6, 8), (7, 8)]. 

##### **Output** 

Choose the most appropriate node as source node of the diameter path: 7. Calculating the longest path among all the shortest paths from the graph and source node 7. The neighboring nodes of the node 7: [8]. Update the shortest path from source node to node [8] with distance 1. The neighboring nodes of the node 8: [6, 7]. Update the shortest path from source node to node [6] with distance 2. The neighboring nodes of the node 6: [3, 4, 8]. Update the shortest path from source node to node [3, 4] with distance 3. The neighboring nodes of the node 3: [1, 2, 4, 6]. Update the shortest path from source node to node [1, 2] with distance 4. The neighboring nodes of the node 1: [0, 3]. Update the shortest path from source node to node [0] with distance 5. The neighboring nodes of the node 0: [1, 9]. Update the shortest path from source node to node [9] with distance 6. The neighboring nodes of the node 9: [0, 5]. Update the shortest path from source node to node [5] with distance 7. The farthest target from the source 7 is node 5 with distance 7. The diameter path is [7, 8, 6, 3, 1, 0, 9, 5]. 

31 

#### Table 14: An example of the Maximum Clique Problem task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. I’ll give an instance of a graph, please help me find the maximum clique in the graph and list the steps and results for each iteration. The Maximum Clique Problem is an optimization problem in graph theory that aims to identify the largest set of vertices in a graph, where every two vertices in the set are adjacent. 

##### **Input** 

The graph has 9 nodes. The nodes are numbered from 0 to 8, and the edges are: [(2, 8), (3, 6), (4, 5), (5, 7)]. 

##### **Output** 

Add the most appropriate node: 8. The current clique is: [8]. The common neighbors of nodes in the current clique are: [2]. Add the most appropriate node: 2. The current clique is: [8, 2]. Finished! The maximum clique is [8, 2]. 

Table 15: An example of the Traveling Salesman Problem task. 

##### **Task Description** 

In an undirected graph, (i,j,k) means that node i and node j are connected with an undirected edge with weight k. I’ll give an instance of a graph, please help me find the solution of the TSP problem in the given graph and list the steps and results for each iteration. The Traveling Salesman Problem (TSP) is a classic combinatorial optimization problem where, given a set of cities(nodes), the goal is to find the shortest possible route that visits each city(node) exactly once and returns to the starting city(node). For each iteration, please select the most appropriate node considering it’s distance from the previous node and it’s influence of total travel distance. 

##### **Input** 

The graph has 7 nodes. The nodes are numbered from 0 to 6, and the edges are: [(0, 1, 8309), (0, 2, 3986), (0, 3, 2254), (0, 4, 1983), (0, 5, 396), (0, 6, 2655), (1, 2, 1416), (1, 3, 9346), (1, 4, 3061), (1, 5, 3220), (1, 6, 7309), (2, 3, 8945), (2, 4, 6117), (2, 5, 9132), (2, 6, 4310), (3, 4, 7830), (3, 5, 1095), (3, 6, 3040), (4, 5, 9538), (4, 6, 6771), (5, 6, 1899)]. 

##### **Output** 

Choose starting node: 0. Choose node 4 after node 0 with weight 1983. The current subtour is [0, 4]. Choose node 1 after node 4 with weight 8309. The current subtour is [0, 4, 1]. Choose node 2 after node 1 with weight 6117. The current subtour is [0, 4, 1, 2]. Choose node 6 after node 2 with weight 7309. The current subtour is [0, 4, 1, 2, 6]. Choose node 3 after node 6 with weight 8945. The current subtour is [0, 4, 1, 2, 6, 3]. Choose node 5 after node 3 with weight 1899. The current subtour is [0, 4, 1, 2, 6, 3, 5]. Choose node 0 after node 5 with weight 2254. The current subtour is [0, 4, 1, 2, 6, 3, 5, 0]. Finished! The optimal solution of TSP is: [0, 4, 1, 2, 6, 3, 5, 0]. 

32 

Table 16: An example of the Maximum Common Subgraph task. 

**Task Description** In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge, we call i and j are neighbors. Please find the maximum common subgraph of two graphs and list the steps and results for each iteration. The maximum common subgraph problem is defined as follows: given two graphs G and H, the task is to find a maximum subgraph sub_g of G and a subgraph sub_h of H such that sub_g and sub_h are isomorphic. That means some nodes of G and H should be put in the nodes lists sub_g_nodes and sub_h_nodes respectively satisfying the following 3 simple requirements. Firstly, sub_g_nodes and sub_h_nodes has the equal length. Secondly, any two nodes in sub_g_nodes or sub_h_nodes are different. Thirdly, for any available indices i and j, if (sub_g_nodes[i], sub_g_nodes[j]) is an edge of G, then (sub_h_nodes[i], sub_h_nodes[j]) must be also an edge of H, and vice versa. The objective is to maximize the length of sub_g_nodes. For each iteration, please choose a node u of G and another node v of H such that the indices of u’neighbors in sub_g_nodes must be same to the indices of v’s neighbors in sub_h_nodes. 

##### **Input** 

The graph G has 5 nodes, the nodes are numbered from 0 to 4, and the edges are: [(0, 4), (1, 2), (1, 3), (1, 4), (3, 4)]. The graph H has 5 nodes, the nodes are numbered from 0 to 4, and the edges are: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 4)]. 

##### **Output** 

Choose node 0 of G, and node 3 of H that has a similar neighborhood structure. The current nodes lists of subgraphs are: [0], [3]. In sub_g_nodes, node 1 does not connect any node. In sub_h_nodes, node 2 does not connect any node. So choose node 1 of G, and node 2 of H as indices of their individual neighbors in the corresponding nodes lists are the same. The current nodes lists of subgraphs are: [0, 1], [3, 2]. In sub_g_nodes, node 3 connects nodes of indices [1] which are [1] in G, and does not connect nodes of indices [0] which are [0] in G. In sub_h_nodes, node 4 connects nodes of indices [1] which are [2] in H, and does not connect nodes of indices [0] which are [3] in H. So choose node 3 of G, and node 4 of H as indices of their individual neighbors in the corresponding nodes lists are the same. 

The current nodes lists of subgraphs are: [0, 1, 3], [3, 2, 4]. In sub_g_nodes, node 4 connects all nodes which are [0, 1, 3] in G. In sub_h_nodes, node 1 connects all nodes which are [2, 3, 4] in H. So choose node 4 of G, and node 1 of H as indices of their individual neighbors in the corresponding nodes lists are the same. 

The current nodes lists of subgraphs are: [0, 1, 3, 4], [3, 2, 4, 1]. Finished! The optimal solution of MCS is: [0, 1, 3, 4], [3, 2, 4, 1]. 

33 

Table 17: An example of the Graph Edit Distance task. 

##### **Task Description** 

In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge, we call i and j are neighbors. Next, I’ll give you two special graphs, where each node has a label. You are required to solve the Graph Edit Distance problem between two graphs. The problem is to establish a one-to-one mapping between nodes from graph G to graph H, ensuring that each node in graph G corresponds to exactly one node in graph H, vice versa. For convenience, the notation i j denotes one node mapping from node i in graph G to node j in graph H, also abbreviated as map(i)=j. For the node mapping i j, if labels of node i and node j are the same, then the cost associated with i j is 0, otherwise the cost is 1. For any two node mapping i j and p q from graph G to graph H, if (i,p) is an edge of G and (j,q) is not an edge of H, then i j and p q incur an edge deletion cost of 1, else if (i,p) is not an edge of G and (j,q) is an edge of H, then the edge insertion cost is 1, otherwise the edge cost is 0. The total cost is the sum of all node mapping costs and all edge costs. The objective is to minimize the total cost of a node mapping from G to H. You should represent the node mapping with an integer list L, such that node i L[i] for all i. For instance, if node 0 in graph G corresponds to node 1 in graph H, node 1 in graph G corresponds to node 0 in graph H, and node 2 remains unchanged, the mapping would be represented as [1, 0, 2, ...]. 

##### **Input** 

The graph G has 5 nodes, the nodes are: [(0, ’Si’), (1, ’O’), (2, ’Si’), (3, ’Na’), (4, ’S’)], and the edges are: [(0, 2), (0, 4), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)]. The graph H has 5 nodes, the nodes are: [(0, ’C’), (1, ’Na’), (2, ’N’), (3, ’Mg’), (4, ’N’)], and the edges are: [(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (2, 4)]. 

##### **Output** 

Mapping node 0 labeled <Si>of graph G to node 4 labeled <N>of graph H. As the mapping two nodes 0 4 have different labels, the node mapping cost adds 1. The current mapping is [4] with cost 1. Mapping node 1 labeled <O>of graph G to node 0 labeled <C>of graph H. As the mapping two nodes 1 0 have different labels, the node mapping cost adds 1. The current mapping is [4, 0] with cost 2. Mapping node 2 labeled <Si>of graph G to node 2 labeled <N>of graph H. As the mapping two nodes 2 2 have different labels, the node mapping cost adds 1. The current mapping is [4, 0, 2] with cost 3. Mapping node 3 labeled <Na>of graph G to node 1 labeled <Na>of graph H. As the mapping two nodes 3 1 have the same label, the node mapping cost adds 0. Currently for any index u of [0], node u does not connect node 3 in graph G, but map(u)=L[u] connects to map(3)=1 in graph H, so the new node mapping 3 1 generate edge addition cost 1. The current mapping is [4, 0, 2, 1] with cost 4. Mapping node 4 labeled <S>of graph G to node 3 labeled <Mg>of graph H. As the mapping two nodes 4 3 have different labels, the node mapping cost adds 1. Currently for any index u in [0], node u connects node 4 in graph G, but map(u)=L[u] does not connect to map(4)=3 in graph H, so the new node mapping 4 3 generate edge deletion cost 1. The current mapping is [4, 0, 2, 1, 3] with cost 6. Finished! The optimal mapping of GED is: [4, 0, 2, 1, 3]. 

34 

