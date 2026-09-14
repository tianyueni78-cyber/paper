# **Can Language Models Solve Graph Problems in Natural Language?** 

**Heng Wang**<sup>_∗_1</sup> **, Shangbin Feng**<sup>_∗_2</sup> **, Tianxing He**<sup>2</sup> **, Zhaoxuan Tan**<sup>3</sup> **, Xiaochuang Han**<sup>2</sup> **, Yulia Tsvetkov**<sup>2</sup> 1Xi’an Jiaotong University 2University of Washington 3University of Notre Dame `wh2213210554@stu.xjtu.edu.cn` , `shangbin@cs.washington.edu` 

## **Abstract** 

Large language models (LLMs) are increasingly adopted for a variety of tasks with _implicit graphical structures_ , such as planning in robotics, multi-hop question answering or knowledge probing, structured commonsense reasoning, and more. While LLMs have advanced the state-of-the-art on these tasks with structure implications, whether LLMs could explicitly process textual descriptions of graphs and structures, map them to grounded conceptual spaces, and perform structured operations remains underexplored. To this end, we propose NLGraph (Natural Language Graph), a comprehensive benchmark of graph-based problem solving designed in natural language. NLGraph contains 29,370 problems, covering eight graph reasoning tasks with varying complexity from simple tasks such as connectivity and shortest path up to complex problems such as maximum flow and simulating graph neural networks. We evaluate LLMs (GPT-3/4) with various prompting approaches on the NLGraph benchmark and find that 1) language models _do_ demonstrate preliminary graph reasoning abilities, 2) the benefit of advanced prompting and in-context learning diminishes on more complex graph problems, while 3) LLMs are also (un)surprisingly brittle in the face of spurious correlations in graph and problem settings. We then propose Build-a-Graph Prompting and Algorithmic Prompting, two instruction-based approaches to enhance LLMs in solving natural language graph problems. Build-a-Graph and Algorithmic prompting improve the performance of LLMs on NLGraph by 3.07% to 16.85% across multiple tasks and settings, while how to solve the most complicated graph reasoning tasks in our setup with language models remains an open research question. The NLGraph benchmark and evaluation code are available at https://github.com/Arthur-Heng/NLGraph. 

## **1 Introduction** 

Originally designed for textual data, large language models (LLMs) are increasingly leveraged for tasks beyond language processing. In robotics and planning, LLMs are adopted to guide agents through structured environments [Huang et al., 2022, Andreas, 2022]. In theory-of-mind reasoning, LLMs are required to maintain and update local and global graphs that reflect the beliefs of different characters [Adhikari et al., 2020, Ammanabrolu and Riedl, 2021]. In structured commonsense reasoning, LLMs are expected to generate graph-based action plans to achieve objectives with diversified prerequisites [Tandon et al., 2019, Madaan et al., 2022]. In multi-hop question answering, LLMs implicitly find connections and paths among a vast network of entities and concepts [Creswell et al., 2023]. Together these works demonstrate that LLMs are widely adopted for tasks with _implicit graphical structures_ while achieving preliminary success. However, one underlying yet crucial question remains underexplored: _Can LLMs reason with graphs?_ More concretely, _are LLMs capable of mapping textual descriptions of graphs and structures to grounded conceptual spaces and solving_ 

> _∗_ equal contribution 

37th Conference on Neural Information Processing Systems (NeurIPS 2023). 

_graph algorithm problems explicitly with natural language?_ The answer to this question has profound implications for large language model applications with implicit graphs and structures, the reasoning ability of LLMs in advanced and graph-based settings, and more. 

To this end, we propose the Natural Language Graph (NLGraph) benchmark, a comprehensive testbed of graph and structured reasoning designed for language models and in natural language. NLGraph contains a total of 29,370 problems, covering eight graph reasoning tasks with varying complexity from intuitively simple tasks such as _connectivity_ , _cycle_ , and _shortest path_ to more complex problems such as _topological sort_ , _maximum flow_ , _bipartite graph matching_ , _Hamilton path_ , and _simulating graph neural networks_ . We control for problem difficulty through generated graph size, network sparsity, numeric range, and more, presenting easy, medium, and hard subsets in each distinct graph reasoning task to enable fine-grained analysis. In addition to using exact match accuracy as a standard metric, we also design several partial credit solutions for various graph reasoning tasks. 

With the NLGraph benchmark, we evaluate whether various large language models [Brown et al., 2020, Ouyang et al., 2022, Bubeck et al., 2023] could perform graph-based reasoning and whether different prompting techniques [Brown et al., 2020, Wei et al., 2022, Kojima et al., 2022, Zhou et al., 2023, Wang et al., 2023] improve the graph reasoning abilities of large language models. Extensive experiments on the NLGraph benchmark demonstrate that: 

1. **LLMs** **_do_ possess preliminary graph reasoning abilities.** Specifically, large language models demonstrate an impressive level of performance that is 37.33% to 57.82% above the random baseline on simple graph reasoning tasks such as connectivity, cycle, and shortest path. With chain-of-thought prompting, LLMs could generate intermediate steps that are sound and accurate while further improving task performance. 

2. **The benefit of advanced prompting methods diminishes with complex problems.** On one hand, chain-of-thought [Wei et al., 2022], least-to-most [Zhou et al., 2023], and self-consistency [Wang et al., 2023] successfully enhance the graph reasoning abilities of LLMs on simple tasks such as cycle and shortest path. On the other hand, these approaches are mostly ineffective, even counterproductive in certain settings, on more complex graph reasoning problems such as topological sort and Hamilton path. 

3. **Learning from examples did not happen on complex graph reasoning problems.** While in-context learning is widely credited for teaching LLMs to learn from examples [Brown et al., 2020], its benefit on more advanced graph reasoning tasks is unclear: Few-shot in-context learning fails to improve over zero-shot prompting across multiple tasks, while increasing the number of exemplars may even be counterproductive for tasks such as Hamilton path. 

4. **LLMs are (un)surprisingly brittle to spurious correlations in problem settings.** We find that in two special cases in the connectivity task (chain and clique), LLMs perform much worse than the general dataset with a performance drop of more than 40% across various settings. This indicates that large language models are implicitly relying on certain spurious correlations (for example, use node mention frequency to determine connectivity), falling short of performing robust structured reasoning in graph-based contexts. 

To improve large language models as better graph reasoners, we propose two instruction-based prompting approaches to better elicit the graph reasoning abilities of large language models. _Builda-Graph prompting_ encourages LLMs to map the textual descriptions of graphs and structures to grounded conceptual spaces [Patel and Pavlick, 2022] before tackling the specific problem through a one-sentence instruction, while _Algorithmic prompting_ instructs LLMs to revisit the algorithmic steps for a given task before learning from in-context exemplars. Experiments demonstrate that builda-graph and algorithmic prompting successfully empower LLMs to better tackle graph reasoning problems, resulting in 3.07% to 16.85% performance gains across multiple tasks, while the most complicated graph reasoning problems remain an open research question. 

## **2 The NLGraph Benchmark** 

To examine whether language models are capable of reasoning with graphs and structures, we curate and propose the Natural Language Graph (NLGraph) benchmark. Specifically, we first employ a random graph generator to generate graphs and structures while controlling for the network size, graph sparsity, and more. We then adopt the generated graphs as bases to synthetically generate problems for eight graph-based reasoning tasks with varying algorithmic difficulties. We control for 

2 



<!-- Start of picture text -->
1. Connectivity 2. Cycle 3. Topological Sort 4. Shortest Path<br>0 2 1 43 5 0 2 1 5 4 3 1 0 2 4 3 0 1 22 1 1 3 1 2 4<br>Determine if there is a path between  In an undirected graph, (i,j) means that  In an undirected graph, the nodes are<br>two nodes in the graph. Note that (i,j)  node i and node j are connected with an  In a directed graph with 5 nodes  numbered from 0 to 4, and the edges are:<br>means that node i and node j are  undirected edge. numbered from 0 to 4: an edge between node 0 and node 1 with<br>connected with an undirected edge. The nodes are numbered from 0 to 5,  node 0 should be visited before node  weight 2, ...<br>Graph: (0,1) (1,2) (3,4) (4,5) and the edges are: (3,4) (3,5) (1,0) (2,5)  4, ... Q : Give the shortest path from node 0 to<br>Q : Is there a path between node 1 and  (2,0) Q : Can all the nodes be visited? Give the  node 4.<br>node 4? Q : Is there a cycle in this graph? solution.<br>5. Maximum Flow 6. Bipartite Graph Matching 7. Hamilton Path 8. GNN<br>1 10 0 6 2 4 3 job applicantsjobs 0 0 1 1 2 2 3 3 4 0 2 1 3 4 0 1 1 1 0 0 1 2 1 0 4 11 3 1<br>There are 4 job applicants numbered<br>In a directed graph, the nodes are  from 0 to 3, and 5 jobs numbered from  In an undirected graph, (i,j) means that  In an undirected graph, the nodes are<br>numbered from 0 to 3, and the edges are: 0 to 4. Each applicant is interested in some of the jobs. Each job can only  node i and node j are connected with an undirected edge. numbered from 0 to 4, and every node has an embedding. (i,j) means that node i and node j<br>an edge from node 1 to node 0 with  accept one applicant and a job  The nodes are numbered from 0 to 4,  are connected with an undirected edge.<br>capacity 10, applicant can be appointed for only one  and the edges are: (4,2) (0,4) (4,3) (0,1)  Embeddings: node 0: [1,1],  …<br>an edge from node 0 to node 2 with  job. (0,2) (4,1) (2,3) The edges are: (0,1) ...<br>capacity 6, Applicant 0 is interested in job 4, ... Q : Is there a path in this graph that  In a simple graph convolution layer, each<br>an edge from node 2 to node 3 with  Q : Find an assignment of jobs to  visits every node exactly once? If yes,  node's embedding is updated by the sum of<br>capacity 4. applicants in such that the maximum  give the path. Note that in a path,  its neighbors' embeddings.<br>Q 1 to node 3?: What is the maximum flow from node  number of applicants find the job they are interested in. adjacent nodes must be connected with edges. Q one layer of simple graph convolution layer?: What's the embedding of each node after<br><!-- End of picture text -->

Figure 1: Overview of the NLGraph Benchmark, featuring eight tasks with varying complexity. We show an intuitive figure representing each task along with the example natural language prompts being passed to the LLMs. 

problem difficulty within each of the eight tasks, resulting in easy, medium, and hard subsets in each graph reasoning task to enable difficulty scaling and fine-grained analysis. 

### **2.1 Random Graph Generator** 

We first employ a general-purpose random graph generator to generate base graphs while using the number of nodes and graph density to control for complexity. Formally, to generate a graph _G_ = _{V, E}_ where _V_ and _E_ denote the set of nodes and edges, we specify the number of nodes _n_ , thus _V_ = _{v_ 1 _, v_ 2 _, . . . , vn}_ , and _|V|_ = _n_ . We then specify the edge probability _p_ such that all the edges are generated according to _P_ ( _eij ∈E_ ) = _p_ , where _eij_ is an edge from _vi_ to _vj_ . The edges could be directed or undirected depending on the task. We use varying _n_ and _p_ values to control for the complexity of the random graph structure. Building on top of these generated base graphs, we also adopt graph edits and other difficulty control factors tailored for each task. 

### **2.2 Tasks** 

Armed with the general-purpose random graph generator, we adapt the synthetically generated graphs to eight graph reasoning tasks with varying complexity and describe the problem setups in natural language. Specifically, we first generate easy, medium, and hard subsets of base graphs for each task by controlling for node amount and graph sparsity. We then adapt or edit the base graphs for each task and design queries accordingly. We present an overview of the NLGraph benchmark with specific natural language instructions in Figure 1. 

- **Task 1: Connectivity** In an undirected graph _G_ = _{V, E}_ , two nodes _u_ and _v_ are _connected_ if there exists a sequence of edges from node _u_ to node _v_ in _E_ . We randomly select two nodes in the base graphs _u, v ∈V_ to ask whether node _u_ and node _v_ are connected with a true/false question. We retain a balanced set of questions where half of the node pairs are connected and the other half are not connected by discarding additional questions. 

- **Task 2: Cycle** In an undirected graph _G_ = _{V, E}_ , a cycle is a non-empty trail ( _e_ 1 _, e_ 2 _, . . . , en_ ) with a node sequence ( _v_ 1 _, v_ 2 _, . . . , vn, v_ 1). We present an undirected graph _G_ = _{V, E}_ to ask whether there exists a cycle through true/false questions. We retain base graphs without cycles as the False subset, while we randomly add edges to these base graphs to generate graphs with cycles as the True subset. We retain a balanced set of cyclic and noncyclic graphs in the dataset. 

- **Task 3: Topological Sort** A topological sort of a directed graph is a linear ordering of its nodes such that for every directed edge ( _u, v_ ) from node _u_ to node _v_ , _u_ comes before _v_ in the ordering. 

3 

|**Subset**|**Connect.**|**Cycle**|**Topo. Sort**|**Shortest Path**|**Max. Flow**|**Bipartite Graph**|**Hamilton Path**|**GNNs**|
|---|---|---|---|---|---|---|---|---|
|# EASY|352 / 730|150 / 300|180 / 360|180 / 360|150 / 300|300 / 600|150 / 300|100 / 200|
|SPEC.|_n_: 5-10|_n_: 5-10|_n_: 5-10|_n_: 5-10|_n_: 5-10|_n_: 6-20|_n_: 5-10|_n_: 5-8|
|# MEDIUM|1,200 / 8,580|600 / 1,800|150 / 1,350|/|/|/|/|/|
|SPEC.|_n_: 11-25|_n_: 11-25|_n_: 11-25|/|/|/|/|/|
|# HARD|680 / 7,090|400 / 2,000|200 / 1,200|200 / 1,200|200 / 1,200|210 / 1,260|200 / 600|140 / 840|
|SPEC.|_n_: 26-35|_n_: 26-35|_n_: 26-35|_n_: 11-20|_n_: 11-20|_n_: 17-33|_n_: 11-20|_n_: 9-15|



Table 1: Statistics of the NLGraph benchmark. We use A / B to indicate that there are A and B problems in the standard and extended set of NLGraph. SPEC. denotes difficulty specifications. 

The task is to find a valid topological sort given a directed graph and there could be multiple valid solutions. We ask LLMs to generate a valid topological sort for the given directed graph and employ an external program to examine its correctness. 

- **Task 4: Shortest Path** The shortest path between two nodes is the path with the sum of edge weights minimized. Given an undirected graph _G_ = _{V, E}_ , a positive weight _w_ for each edge, and two nodes _u_ and _v_ , the task is to find the shortest path between node _u_ and node _v_ and its corresponding path length. We filter the generated base graphs by specifying that the number of nodes on the correct shortest path is as least _ℓ_ , where _ℓ_ is chosen from _ℓmin_ to _ℓmax_ for each question to sever as an additional difficulty control measure. We adopt two metrics: _exact match_ , where the LLM solution is a valid path and optimal, and _partial credit_ , where the LLM solution is valid and is the rank _i_ -th shortest among all the possible paths (i.e. the number of shorter paths plus one). The partial credit score for each problem can be formulated as PC = 1 _/_ rank _i_ . 

- **Task 5: Maximum Flow** Let _G_ = _{V, E}_ be a network with two nodes _s, t ∈V_ being the source and the sink. Each edge is associated with a capacity _c_ , the maximum amount of flow that can pass through the edge. We ask LLMs to generate a plan to route as much flow as possible from the source to the sink. We evaluate in both exact match with the optimal plan and partial credit for this 

if _t ≤ s_ task, where partial credit can be formulated as PC = �0 _t/s,,_ if _t > s_<sup>, where</sup><sup>_s_is the flow value</sup> under the optimal plan, and _t_ is the flow value of the solution generated by LLMs. 

- **Task 6: Bipartite Graph Matching** In an undirected graph _G_ = _{V, E}_ , a matching is a set of edges without common nodes. A bipartite graph is a graph whose nodes can be divided into two disjoint sets **U** and **V** , and in each set no nodes are adjacent to each other. Given a bipartite graph, the task is to find the matching that maximizes the number of edges. We use an external program to evaluate whether the solution generated by LLMs is valid and optimal. 

- **Task 7: Hamilton Path** In an undirected graph, a Hamilton path is a path that visits every node exactly once. Given an undirected graph _G_ = _{V, E}_ , the task is to find a valid Hamilton path. We filter generated base graphs to ensure that at least one valid Hamilton path exists and use an external program to evaluate the LLM solution. 

- **Task 8: Graph Neural Networks** Given an undirected graph _G_ = _{V, E}_ , and a two-dimension node embedding **x** _i_ for each node, the task is to perform _ℓ_ layers of message passing, _i.e._ to = 

- update the node embedding with the sum of all the neighbors’ embeddings. Formally, **x**<sup>(</sup> _i_<sup>_ℓ_+1)</sup> � _j∈Ni_<sup>**x**(</sup> _j_<sup>_ℓ_)</sup> where _Ni_ denotes the neighborhood of node _i_ and ( _ℓ_ ) denotes the _ℓ_ -th layer. We use an exact match with the correct node embeddings and two types of partial credits for this task. Specifically, the first partial credit is the percentage of the nodes whose embedding is correct (PC), and the second is the average of all the values’ relative errors for the standard answer (RE). The _<u>|x−y|</u>_ 

- relative error is formulated as _RE_ = max( _x,y_ )<sup>, where</sup><sup>_x_is the value generated by LLMs and</sup><sup>_y_is</sup> the value in the standard answer, averaged across all embedding dimensions. 

### **2.3 Benchmark Statistics** 

Using the above methodology, we generate the NLGraph benchmark with 5,902 problems in a standard version and 29,370 problems in an extended version. Intuitively easier tasks, including connectivity, cycle, and topological sort problems, are further divided into easy, medium, and hard subsets based on graph size, sparsity, among other difficulty control factors. More algorithmically advanced tasks, including shortest path, maximum flow, bipartite graph matching, Hamilton path, 

4 

|**Method**||**Connec**|**tivity**|||**Cyc**|**le**||||**Shortest P**|**ath**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Easy**|**Medium**|**Hard**|**Avg.**|**Easy**|**Medium**|**Hard**|**Avg.**|**Easy**|**Hard**|**Easy (PC)**|**Hard (PC)**|**Avg.**|
|RANDOM|50.00|50.00|50.00|50.00|50.00|50.00|50.00|50.00|6.07|6.69|14.73|13.81|17.81|
|ZERO-SHOT|83.81|72.75|63.38|71.31|50.00|50.00|50.00|50.00|29.40|21.00|46.00|26.76|30.79|
|FEW-SHOT|93.75|83.83|76.61|84.73|80.00|**70.00**|**61.00**|**70.33**|31.11|26.00|49.19|35.73|35.51|
|COT|**94.32**|82.17|77.21|84.57|**84.67**|63.33|53.25|66.75|63.89|**29.50**|76.84|35.79|51.51|
|0-COT|79.55|65.83|68.53|71.30|55.33|57.67|49.00|54.00|8.89|7.50|62.39|**43.95**|32.03|
|COT+SC|93.18|**84.50**|**82.79**|**86.82**|82.00|63.67|53.50|66.39|**68.89**|29.00|**80.25**|38.47|**54.15**|



Table 2: Model performance on the connectivity, cycle, and shortest path tasks. PC denotes partial credit. Large language models with COT or COT+SC prompting greatly outperforms the random baseline by 37.33% to 57.82%, indicating that LLMs have preliminary graph reasoning abilities. 

and graph neural networks problems, are divided into easy and hard subsets. We present benchmark statistics in Table 1. Accuracy (whether the true/false answer is correct, whether the proposed solution is valid) is the default evaluation metric, while tasks 4, task 5, and task 8 have additional partial-credit metrics aforementioned. We envision NLGraph as a comprehensive testbed for graph and structured reasoning for large language models. 

## **3 Experimental Settings** 

Based on the NLGraph benchmark, we aim to investigate _whether language models can solve graph algorithm problems in natural language_ by evaluating large language models and different prompting approaches. 

**Baselines** We adopt a wide range of prompting approaches as baselines. Specifically, zero-shot prompting (ZERO-SHOT), few-shot in-context learning (FEW-SHOT) [Brown et al., 2020], chain-ofthought prompting (COT) [Wei et al., 2022], zero-shot chain-of-thought (0-COT) [Kojima et al., 2022], least-to-most (LTM) [Zhou et al., 2023], and self-consistency (SC) [Wang et al., 2023] are leveraged to tackle various graph reasoning tasks in the NLGraph benchmark. 

We also adopt a RANDOM baseline: for true/false questions such as connectivity and cycle, we use RANDOM to denote a baseline that randomly selects an answer from true and false with an expected accuracy of 50%; For the shortest path task, RANDOM denotes a baseline that randomly selects a valid path between the query node pair. For the maximum flow task, RANDOM denotes a baseline that randomly selects a value between 0 and the sum of all the edges’ capacities. The performance comparison between different prompting techniques and the RANDOM baseline could indicate whether LLMs are capable of performing graph reasoning instead of giving randomly generated answers. 

**Models and Settings** We use TEXT-DAVINCI-003 as the default large language model, while we also evaluate three additional LLMs (GPT-3.5-TURBO, CODE-DAVINCI-002, and GPT-4), presenting results in Appendix E. For all baselines except self-consistency, we set temperature _τ_ = 0; For self-consistency prompting, we sample five chain-of-thought responses with temperature _τ_ = 0 _._ 7. For few-shot prompting techniques (i.e., FEW-SHOT, COT, LTM, and COT+SC), the input prompt includes _k_ exemplars selected from the extended version before the problem of interest. For the connectivity task and cycle task, we set _k_ to 4, for the GNN task, we set _k_ to 1 due to the context size limit, while for other tasks _k_ is 5. We evaluate LLMs and various prompting techniques on the standard set of NLGraph due to monetary costs, while we encourage future research to leverage the extended version for enhanced evaluation. 

## **4 Results** 

### **4.1 LLMs Have (Preliminary) Graph Reasoning Abilities** 

We first find that on intuitively simple graph reasoning tasks, large language models achieve impressive performance and demonstrate preliminary graph reasoning abilities. As demonstrated in Table 2, LLM performance on the connectivity, cycle, and shortest path tasks is significantly better than the RANDOM baseline, indicating that LLMs are not giving random answers and they _do_ have preliminary graph reasoning abilities. In the first two tasks with true/false questions, LLM performance is 37.33% to 57.82% higher than random with COT or COT+SC prompting. The performance is also impressive 

5 



<!-- Start of picture text -->
75 70.6 20<br>50 51.7 54.4 50.5 easy 15.3 12.0 easy<br>36.1 37.8 10 9.3 10.0<br>25 4.0<br>0 0<br>zero-shot few-shot 0-CoT CoT CoT+SC LTM zero-shot few-shot 0-CoT CoT CoT+SC<br>20 18.4 10<br>medium hard<br>10 5 4.0<br>5.1 2.5 2.0 2.0<br>1.1 0.9 1.6 0.2 1.0<br>0 0<br>zero-shot few-shot 0-CoT CoT CoT+SC LTM zero-shot few-shot 0-CoT CoT CoT+SC<br>topological sort maximum flow<br>Acc Acc<br>Acc Acc<br><!-- End of picture text -->

Figure 2: (left) Model performance on the topological sort task. COT, LTM, and self-consistency are mostly ineffective on this problem. (right) Model performance on the maximum flow task. FEW-SHOT prompting outperforms COT+SC prompting on both easy and hard subsets, suggesting that LLMs fall short of generating valid intermediate steps to solve the more complex graph reasoning problem. Together these results demonstrate that advanced prompting is ineffective for advanced graph reasoning. 

in the ZERO-SHOT setting, as the accuracy is 33.81% and 23.33% higher on the connectivity and shortest path task than random even without any exemplars and chain-of-thought reasoning. Though the shortest path is intuitively harder than the first two true/false tasks since it requires generating the specific shortest path in the response, LLM combined with COT and COT+SC achieves an accuracy 22.81% to 62.83% higher than RANDOM. Together these results demonstrate that large language models _do_ possess preliminary abilities to process graphs and structures in input texts. 

### **4.2 Mixed Results with Advanced Prompting** 

Table 2 shows that advanced prompting techniques such as chain-of-thought [Wei et al., **Method** PC ( _↑_ ) ACC ( _↑_ ) RE ( _↓_ ) 2022] and self-consistency [Wang et al., 2023] ZERO-SHOT 13.61 0.00 20.04 successfully improve performance on simple FEW-SHOT 20.04 0.00 37.83 graph reasoning tasks. For the task of simuCOT **64.55 31.00** 14.34 lating graph neural networks (Table 3), chain0-COT 13.85 0.00 44.55 of-thought also significantly improves model COT+SC 63.92 28.00 **13.28** performance. However, these approaches can be ineffective, even counterproductive on more Table 3: Model performance on the task of simucomplex graph reasoning tasks. From the results lating graph neural networks. PC and RE are two on the topological sort and maximum flow task partial credit metrics introduced in §2.2. Chain(Figure 2), we observe that COT, COT+SC, and of-thought prompting significantly improves the LTM prompting generally underperform FEWmodel performance across all metrics. SHOT prompting. We believe this may be because LLMs fail to learn the correct way to generate intermediate steps in the face of complex graph reasoning tasks. This casts doubt on the generalizability of COT, LTM, and self-consistency to more advanced graph reasoning problems. 

Table 3: Model performance on the task of simulating graph neural networks. PC and RE are two partial credit metrics introduced in §2.2. Chainof-thought prompting significantly improves the model performance across all metrics. 

### **4.3 In-Context Learning Can be Counterproductive** 

Although in-context learning is widely attributed to teaching LLMs to learn from in-context exemplars [Brown et al., 2020], we observe that few-shot in-context learning fails to improve LLM performance over complex graph reasoning problems. For tasks such as Hamilton path and bipartite graph matching (Figure 3), zero-shot prompting generally outperforms few-shot learning with in-context exemplars. The results suggest that LLMs fail to learn from the in-context exemplars when the problem involves hundreds of graph-based reasoning steps. In-context exemplars might even distract large language models, evident in that few-shot learning underperforms zero-shot learning by 1.00% to 10.48% on Hamilton path and bipartite graph matching. We further study the correlation between the number of exemplars and model performance on the Hamilton path task. As illustrated in Figure 4, when the number of exemplars increases, model performance is not trending up, and the performance is consistently lower than zero-shot prompting. These results further suggest that in-context learning could be counterproductive in complex structured reasoning. 

6 



<!-- Start of picture text -->
60 easy hard 60 easy hard<br>49.3 46.7 46.0 45.0 48.3 47.0<br>40.0 40.7<br>40 34.7 40<br>27.6 27.1<br>20 20.0 17.5 14.7 20 17.1 13.3 11.4<br>8.0 8.5<br>4.0<br>0 0<br>zero-shot few-shot 0-CoT CoT CoT+SC zero-shot few-shot 0-CoT CoT CoT+SC<br>Hamilton path bipartite graph matching<br>Acc Acc<br><!-- End of picture text -->

Figure 3: (left) Model performance on the Hamilton path task. ZERO-SHOT prompting consistently outperforms all other prompting techniques. (right) Model performance on the bipartite graph matching task. The effect of in-context learning and advanced prompting is also mostly marginal in this complex graph reasoning problem. Together these results demonstrate that in-context learning can be counterproductive in advanced graph reasoning problems. 

|**Dataset**|ZERO-SHOT|FEW-SHOT|COT|0-COT|COT+SC|Avg.|
|---|---|---|---|---|---|---|
|GENERAL|74.67|83.33|85.33|66.00|82.67|78.40|
|CHAIN|51.67(-23.00)|45.00(-35.33)|40.83(-44.50)|92.50(+26.50)|44.17(-38.50)|54.83(-23.57)|
|CLIQUE|60.83(-13.84)|73.33(-10.00)|85.00(-0.33)|52.50(-13.50)|83.33(+0.66)|71.00(-7.40)|



Table 4: Model performance on the chain and clique subset of the connectivity task. Large language models indeed rely on spurious correlations in problem settings, evident in the reduced performance on the two special cases compared to the general connectivity task. 

### **4.4 LLMs are (Un)surprisingly Brittle** 

Although large language models achieved performance that is significantly better than random on simple graph reasoning tasks (§4.1), we hypothesize that LLMs may be able to reach the correct answer by leveraging certain spurious correlations. For example, on the connectivity task, since nodes with higher degrees are more frequently mentioned and they are more likely to be connected, LLMs might just be counting node mentions instead of actually finding paths. To this end, we design two special cases (chain and clique) for the connectivity task that are the exact opposite of the spurious correlation. 



<!-- Start of picture text -->
60<br>easy hard<br>40<br>20<br>0<br>0 2 4 8 12 16<br># exemplar<br>Acc<br><!-- End of picture text -->

Figure 4: Model performance on the Hamilton path task with an increasing amount of exemplars. When more in-context exemplars are introduced, model performance is not trending up and is consistently lower than zero-shot prompting in both difficulty settings. 

**Chain** We firstly generate a graph with _k_ components, where each components is a chain. Formally, _G_ = _{V, E}_ can be divided into subgraphs _G_ 1 _, G_ 2 _, . . . , Gk_ , where subgraph _Gi_ consists of a chain of nodes and edges _vi_ 1 _, ei_ 1 _, vi_ 2 _, ei_ 2 _, . . . , eiti, viti_ . We then randomly select query node pairs that are at the two ends of a chain, _i.e. vi_ 1 and _viti_ . These nodes only have a degree of one but they are actually connected through the chain structure. We curate a chain dataset with 120 examples. 

**Clique** We first generate a graph with _k_ densely connected subgraphs. Formally, _G_ = _{V, E}_ can be divided into subgraphs _G_ 1 _, G_ 2 _, . . . , Gk_ , where subgraph _Gi_ is generated by the random graph generator (§2.1) with a high edge probability _p ∈{_ 0 _._ 7 _,_ 1 _._ 0 _}_ . We then randomly select query node pairs with each pair in two different densely connected subgraphs, _Gi_ and _Gj_ ( _i̸_ = _j_ ). These nodes are associated with a large number of edges and thus are frequently mentioned in the natural language prompt, but they belong to two different subgraphs and are not connected. We curate a clique dataset with 120 examples. 

We evaluate LLMs with different prompting approaches on the two special cases and compare performances with the general connectivity task in Table 4. LLM performs much worse than ordinary 

7 



<!-- Start of picture text -->
Standard Prompting Build-a-Graph Prompting Algorithmic Prompting<br>We can use a Depth-First Search (DFS) algorithm to<br>0 3 33 114 1 24 2 4 <in-context exemplar>In an undirected graph, the nodes are numbered from 0 to 4, and the edges are:an edge between node 0 and node 4 with weight 4,  … you can keep track of the distance it takes to reachundirected graph.that node from the starting node.find the shortest path between two given nodes in anThe basic idea is to start at one of the nodes and useDFS to explore all of its adjacent nodes. At each node,<br>Once you have explored all the adjacent nodes, you<br><in-context exemplar> Let's construct a graph with the nodes and can backtrack and pick the node which has the<br>In an undirected graph, the nodes are  edges first. shortest distance to reach the destination node.<br>numbered from 0 to 4, and the edges are: <in-context exemplar><br>an edge between node 0 and node 4 with  Q : Give the shortest path from node 0 to  In an undirected graph, the nodes are numbered from<br>weight 4, node 2. 0 to 4, and the edges are:<br>an edge between node 0 and node 3 with  A :   All the paths from node 0 to node 2 are: an edge between node 0 and node 4 with weight 4, ...<br>weight 3, 0,3,2 with a total weight of 3 + 1 = 4, Q : Give the shortest path from node 0 to node 2.<br>an edge between node 0 and node 1 with  0,1,4,2 with a total weight of 3 + 4 + 2 = 9, A :   All the paths from node 0 to node 2 are:<br>weight 3, 0,4,3,2 with a total weight of 4 + 1 + 1 = 6. 0,3,2 with a total weight of 3 + 1 = 4,<br>... The weight of path 0,3,2 is the smallest, so  0,1,4,2 with a total weight of 3 + 4 + 2 = 9,<br>Q : Give the shortest path from node 0 to  the shortest path from node 0 to node 2 is  0,4,3,2 with a total weight of 4 + 1 + 1 = 6.<br>node 2. 0,3,2 with a total weight of 4. The weight of path 0,3,2 is the smallest, so the<br>shortest path from node 0 to node 2 is 0,3,2 with a<br>total weight of 4.<br><!-- End of picture text -->

Figure 5: Overview of Build-a-Graph prompting and Algorithmic prompting, aiming to make LLMs better at reasoning with graphs by encouraging conceptual grounding and algorithmic reflection. Red underline indicates our proposed instructions while green background indicates LLMs’ generation. 

cases with a performance drop of more than 40% across various settings. This suggests that LLMs are indeed (un)surprisingly vulnerable to spurious correlations in structured reasoning. 

## **5 Making Language Models Better Graph Reasoners** 

### **5.1 Methodology** 

We propose two instruction-based prompting techniques that improve the graph reasoning ability of LLMs, which can be used together with in-context learning and chain-of-thought prompting. 

**Build-a-Graph Prompting (BAG)** We hypothesize that it might be helpful to map the textual descriptions of graphs to grounded conceptual spaces [Patel et al., 2021] before tackling the specific problem, _i.e._ visualizing the graph structure on an implicit mental sketchpad. To this end, we propose to use instruction-based prompting by appending “ _Let’s construct a graph with the nodes and edges first._ ” after the textual description of the graph is explicitly given. We envision this straightforward instruction would provide LLMs with the buffer zone to digest graph information, map them to grounded conceptual spaces, and better prepare for the incoming query. 

**Algorithmic Prompting** We hypothesize that in order to generate sound and accurate solutions, LLMs would benefit from revisiting and reciting the relevant algorithm for a given task [Sun et al., 2023]. To this end, we propose to first prepend the algorithm details before the in-context examples by adding “We can use a Depth-First Search (DFS) algorithm ...” for the shortest path task. We similarly provide the algorithm descriptions of other graph reasoning tasks in their respective prompts. We envision algorithmic prompting as empowering LLMs with a general understanding of how to solve the problem before actually solving it. 

We illustrate our proposed build-a-graph prompting and algorithmic prompting in Figure 5. In the following, we use these two approaches together with chain-of-thought prompting and evaluate on three representative tasks in the NLGraph benchmark with varying difficulties. 

### **5.2 Results** 

Table 5 shows the results of our proposed prompting methods on three representative tasks with varying complexity. On the two easier tasks, cycle and shortest path, our instruction-based prompting methods resulted in a 3.07% to 16.85% performance gain across the two tasks. However, on the more complex task, Hamilton path, the two natural language instructions are largely ineffective. The result suggests that the two simple instruction-based prompting techniques successfully improve LLMs’ graph reasoning abilities on relatively easy graph reasoning tasks, while how to make LLMs better 

8 

|**Method**||**Cyc**|**le**||||**Shortest P**|**ath**||**Ha**|**milton P**|**ath**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Easy**|**Medium**|**Hard**|**Avg.**|**Easy**|**Hard**|**Easy (PC)**|**Hard (PC)**|**Avg.**|**Easy**|**Hard**|**Avg.**|
|COT|84.67|63.33|53.25|66.75|63.89|29.50|76.84|35.79|51.51|**40.00**|**8.00**|**24.00**|
|COT+BAG|**86.00**|69.33|62.00|**72.44**|**67.78**|**33.50**|**79.20**|**42.56**|**55.76**|38.67|6.00|22.34|
|COT+ALGORITHM|77.33|**74.00**|**64.00**|71.78|63.89|28.00|76.06|38.70|51.66|36.67|7.50|22.09|



Table 5: Model performance on the connectivity, cycle, and shortest path tasks with our proposed BAG and ALGORITHM prompting. On the two easier tasks, cycle and shortest path, our instructionbased prompting techniques resulted in a 3.07% to 16.85% performance gain across the two tasks. More complex graph reasoning tasks such as Hamilton path remain an open research question. 

at reasoning on complex graph reasoning problems remains an open research question. We further explore different variants of the instructions in Appendix D. The NLGraph benchmark also empowers the evaluation of future instructions and solutions towards making LLMs better graph reasoners. 

## **6 Related Work** 

**LLMs for tasks with implicit graphical structures.** Previous works explored the use of LLMs on tasks with implicit graph structures: Huang et al. [2022] find that LLMs have the ability to ground high-level tasks (e.g. "make breakfast") to a set of actionable steps (e.g. "open fridge") in structured synthetic environments. Valmeekam et al. [2022] explore the possibility of using LLMs for commonsense planning. In theory-of-mind reasoning, Adhikari et al. [2020], Ammanabrolu and Riedl [2021], Sclar et al. [2023] maintain and update structured world representations as the world state change to operate in interactive and situated environments. In structured commonsense reasoning, where LLMs are given a natural language input and then asked to generate a graph such as an event graph [Tandon et al., 2019], a reasoning-graph [Madaan et al., 2021] or an argument explanation graph [Saha et al., 2021], Madaan et al. [2022] find that a code language model (CODEX) with tasks framed as code generation tasks outperforms other strong LMs. In multi-hop question answering or knowledge probing, LLMs implicitly find connections and paths among a vast network of entities and concepts [Creswell et al., 2023, Yu et al., 2022, Zhang et al., 2022a, He et al., 2021]. Recently, Chen et al. [2023] explore the potential of LLMs on the graph node classification task. Together these works demonstrate that LLMs are increasingly adopted for tasks and settings with implicit graphs and structures, while whether LLMs are robust at graph reasoning remains underexplored and may hinder the progress of these structure-aware applications. In this work, we propose the NLGraph benchmark as a comprehensive testbed towards evaluating the graph reasoning abilities of large language models. 

**LLMs for few-shot reasoning.** There is a long line of work on evaluating LLMs’ reasoning ability in an in-context learning setting, including arithmetic reasoning, logical reasoning, common sense reasoning, and more. Particularly, simple math problem datasets such as AQUA Ling et al. [2017], GSM8K [Cobbe et al., 2021], and SVAMP [Patel et al., 2021] are used for evaluating arithmetic reasoning [He-Yueya et al., 2023, Touvron et al., 2023, Shi et al., 2023]. Welleck et al. [2021] developed NaturalProofs, a multi-domain dataset for studying mathematical reasoning in natural language, while Welleck et al. [2022] study LLMs’ ability to generate the next step in mathematical proof and generate full proofs. LLMs have also been evaluated on logical reasoning tasks, including symbolic tasks like Coin Flip and Last Letter Concatenation [Wei et al., 2022] and Logic Grid Puzzle on the BIG-BENCH [Srivastava et al., 2023]. Commonsense reasoning datasets [Talmor et al., 2019, Geva et al., 2021] are also proposed to evaluate large language models. Most relevant to our work, various proposals to evaluate and augment the algorithm reasoning abilities of large language models are explored [Zhou et al., 2022, Lee and Kim, 2023, Zelikman et al., 2023, Liu et al., 2023]. In this work, we focus on evaluating and enhancing LLMs on graph-based reasoning and algorithmic tasks inspired by the increasing usage of LLMs in tasks with implicit graphs and structures. 

## **7 Conclusion** 

In this work, we investigate whether LLMs are capable of explicit graph reasoning, _i.e._ , solving graph algorithm problems in natural language, across various problem categories and prompting techniques. To this end, we curate the NLGraph benchmark, a comprehensive test bed of graph-based reasoning in natural language, with 29,370 problems covering eight tasks with varying complexity. By evaluating 

9 

LLMs and prompting approaches on the NLGraph benchmark, we find that 1) LLMs do possess preliminary graph reasoning abilities, 2) the benefit of advanced prompting and in-context learning may diminish on complex reasoning tasks, while 3) LLMs are brittle to spurious correlations in problem settings. We then propose Build-a-Graph and Algorithmic Prompting, two simple instructionbased approaches that bring notable performance gains across multiple tasks. Improving LLMs’ graph reasoning abilities on complex and nuanced graph reasoning tasks remains an open research question, and we encourage future work to develop upon our proposed NLGraph benchmark. 

## **Acknowledgements** 

We would like to thank the reviewers, the area chair, Jiacheng Liu, Minnan Luo, and members of the UW NLP Group for their comments and feedback. This material is funded by the DARPA Grant under Contract No. HR001120C0124. We also gratefully acknowledge support from NSF CAREER Grant No. IIS2142739, the Alfred P. Sloan Foundation Fellowship, and NSF grant No. IIS2203097. Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily state or reflect those of the United States Government or any agency thereof. 

## **References** 

- Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In _International Conference on Machine Learning_ , pages 9118–9147. PMLR, 2022. 

- Jacob Andreas. Language models as agent models. In _Findings of the Association for Computational Linguistics: EMNLP 2022_ , pages 5769–5779, Abu Dhabi, United Arab Emirates, December 2022. Association for Computational Linguistics. URL `https://aclanthology.org/2022. findings-emnlp.423` . 

- Ashutosh Adhikari, Xingdi Yuan, Marc-Alexandre Côté, Mikuláš Zelinka, Marc-Antoine Rondeau, Romain Laroche, Pascal Poupart, Jian Tang, Adam Trischler, and Will Hamilton. Learning dynamic belief graphs to generalize on text-based games. _Advances in Neural Information Processing Systems_ , 33:3045–3057, 2020. 

- Prithviraj Ammanabrolu and Mark Riedl. Learning knowledge graph-based world models of textual environments. In A. Beygelzimer, Y. Dauphin, P. Liang, and J. Wortman Vaughan, editors, _Advances in Neural Information Processing Systems_ , 2021. URL `https://openreview.net/ forum?id=o24k_XfIe6_` . 

- Niket Tandon, Bhavana Dalvi, Keisuke Sakaguchi, Peter Clark, and Antoine Bosselut. WIQA: A dataset for “what if...” reasoning over procedural text. In _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_ , pages 6076–6085, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1629. URL `https://aclanthology.org/D19-1629` . 

- Aman Madaan, Shuyan Zhou, Uri Alon, Yiming Yang, and Graham Neubig. Language models of code are few-shot commonsense learners. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ , pages 1384–1403, Abu Dhabi, United Arab Emirates, December 2022. Association for Computational Linguistics. URL `https://aclanthology. org/2022.emnlp-main.90` . 

- Antonia Creswell, Murray Shanahan, and Irina Higgins. Selection-inference: Exploiting large language models for interpretable logical reasoning. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=3Pf3Wg6o-A4` . 

- Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

10 

- Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. _Advances in Neural Information Processing Systems_ , 35: 27730–27744, 2022. 

- Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al. Sparks of artificial general intelligence: Early experiments with gpt-4. _arXiv preprint arXiv:2303.12712_ , 2023. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed H. Chi, Quoc V Le, and Denny Zhou. Chain of thought prompting elicits reasoning in large language models. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, _Advances in Neural Information Processing Systems_ , 2022. URL `https://openreview.net/forum?id= _VjQlMeSB_J` . 

- Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, _Advances in Neural Information Processing Systems_ , 2022. URL `https://openreview.net/forum?id=e2TBb5y0yFf` . 

- Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. Least-to-most prompting enables complex reasoning in large language models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=WZH7099tgfM` . 

- Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=1PL1NIMMrw` . 

- Roma Patel and Ellie Pavlick. Mapping language models to grounded conceptual spaces. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/ forum?id=gJcEM8sxHK` . 

- Arkil Patel, Satwik Bhattamishra, and Navin Goyal. Are NLP models really able to solve simple math word problems? In _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , pages 2080–2094, Online, June 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.naacl-main. 168. URL `https://aclanthology.org/2021.naacl-main.168` . 

- Zhiqing Sun, Xuezhi Wang, Yi Tay, Yiming Yang, and Denny Zhou. Recitation-augmented language models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=-cqvvvb-NkI` . 

- Karthik Valmeekam, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. Large language models still can’t plan (a benchmark for LLMs on planning and reasoning about change). In _NeurIPS 2022 Foundation Models for Decision Making Workshop_ , 2022. URL `https://openreview.net/forum?id=wUU-7XTL5XO` . 

- Melanie Sclar, Sachin Kumar, Peter West, Alane Suhr, Yejin Choi, and Yulia Tsvetkov. Minding language models’ (lack of) theory of mind: A plug-and-play multi-character belief tracker. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 13960–13980, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.780. URL `https://aclanthology.org/2023. acl-long.780` . 

- Aman Madaan, Dheeraj Rajagopal, Niket Tandon, Yiming Yang, and Eduard Hovy. Could you give me a hint ? generating inference graphs for defeasible reasoning. In _Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021_ , pages 5138–5147, Online, August 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.findings-acl.456. URL `https: //aclanthology.org/2021.findings-acl.456` . 

11 

- Swarnadeep Saha, Prateek Yadav, Lisa Bauer, and Mohit Bansal. ExplaGraphs: An explanation graph generation task for structured commonsense reasoning. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , pages 7716–7740, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics. doi: 10.18653/ v1/2021.emnlp-main.609. URL `https://aclanthology.org/2021.emnlp-main.609` . 

- Xinyan Velocity Yu, Sewon Min, Luke Zettlemoyer, and Hannaneh Hajishirzi. Crepe: Open-domain question answering with false presuppositions. _arXiv preprint arXiv:2211.17257_ , 2022. URL `https://arxiv.org/abs/2211.17257` . 

- Xikun Zhang, Antoine Bosselut, Michihiro Yasunaga, Hongyu Ren, Percy Liang, Christopher D Manning, and Jure Leskovec. GreaseLM: Graph REASoning enhanced language models. In _International Conference on Learning Representations_ , 2022a. URL `https://openreview. net/forum?id=41e9o6cQPj` . 

- Tianxing He, Kyunghyun Cho, and James Glass. An empirical study on few-shot knowledge probing for pretrained language models, 2021. 

- Zhikai Chen, Haitao Mao, Hang Li, Wei Jin, Hongzhi Wen, Xiaochi Wei, Shuaiqiang Wang, Dawei Yin, Wenqi Fan, Hui Liu, et al. Exploring the potential of large language models (llms) in learning on graphs. _arXiv preprint arXiv:2307.03393_ , 2023. 

- Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. Program induction by rationale generation: Learning to solve and explain algebraic word problems. In _Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 158–167, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1015. URL `https://aclanthology.org/P17-1015` . 

- Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ , 2021. 

- Joy He-Yueya, Gabriel Poesia, Rose E Wang, and Noah D Goodman. Solving math word problems by combining language models with symbolic solvers. _arXiv preprint arXiv:2304.09102_ , 2023. 

- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H Chi, Nathanael Schärli, and Denny Zhou. Large language models can be easily distracted by irrelevant context. In _International Conference on Machine Learning_ , pages 31210–31227. PMLR, 2023. 

- Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh Hajishirzi, Yejin Choi, and Kyunghyun Cho. Naturalproofs: Mathematical theorem proving in natural language. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 1)_ , 2021. URL `https://openreview.net/forum?id=Jvxa8adr3iY` . 

- Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh Hajishirzi, and Yejin Choi. Naturalprover: Grounded mathematical proof generation with language models. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, _Advances in Neural Information Processing Systems_ , 2022. URL `https://openreview.net/forum?id=rhdfTOiXBng` . 

- Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-Alonso, et al. Beyond the imitation game: Quantifying and extrapolating the capabilities of language models. _Transactions on Machine Learning Research_ , 2023. 

- Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. CommonsenseQA: A question answering challenge targeting commonsense knowledge. In _Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)_ , pages 4149–4158, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics. doi: 10.18653/v1/N19-1421. URL `https: //aclanthology.org/N19-1421` . 

12 

- Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant. Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies. _Transactions of the Association for Computational Linguistics (TACL)_ , 2021. 

- Hattie Zhou, Azade Nova, Hugo Larochelle, Aaron Courville, Behnam Neyshabur, and Hanie Sedghi. Teaching algorithmic reasoning via in-context learning. _arXiv preprint arXiv:2211.09066_ , 2022. 

- Soochan Lee and Gunhee Kim. Recursion of thought: A divide-and-conquer approach to multicontext reasoning with language models. In _Findings of the Association for Computational Linguistics: ACL 2023_ , pages 623–658, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-acl.40. URL `https://aclanthology.org/2023. findings-acl.40` . 

- Eric Zelikman, Qian Huang, Gabriel Poesia, Noah D Goodman, and Nick Haber. Parsel: A (de) compositional framework for algorithmic reasoning with language models. _arXiv preprint arXiv:2212.10561_ , 2023. 

- Chenxiao Liu, Shuai Lu, Weizhu Chen, Daxin Jiang, Alexey Svyatkovskiy, Shengyu Fu, Neel Sundaresan, and Nan Duan. Code execution with pre-trained language models. In _Findings of the Association for Computational Linguistics: ACL 2023_ , pages 4984–4999, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-acl.308. URL `https://aclanthology.org/2023.findings-acl.308` . 

- Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, et al. Opt: Open pre-trained transformer language models. _arXiv preprint arXiv:2205.01068_ , 2022b. 

13 

## **A Discussion** 

**NLP tasks and graph tasks alignment.** Originally designed for processing language, LLMs are increasingly adopted for NLP tasks with structural implications. For instance, structured commonsense reasoning is similar to topological sort in that they both need to find a solution satisfying diversified constraints between entities. In the belief state graph in theory-of-mind [Adhikari et al., 2020, Ammanabrolu and Riedl, 2021], the final task is to determine the connectivity of nodes, which corresponds to the connectivity task. In multi-hop question answering [Creswell et al., 2023], LLMs implicitly find connections and paths among a vast network of entities and concepts, which resembles the shortest path task and connectivity task. However, we acknowledge that not all graph reasoning tasks in the NLGraph benchmark are clearly aligned with certain applications, thus advanced graph reasoning tasks in the NLGraph benchmark could also be viewed as a test of language model reasoning ability. 

**The NLGraph benchmark envisioned as reasoning benchmark.** In addition to evaluating graph reasoning abilities, the NLGraph benchmark can also be viewed as a structural benchmark to evaluate language model reasoning. While ample LM reasoning datasets exist [Cobbe et al., 2021, Patel et al., 2021, Talmor et al., 2019], it is difficult to avoid train-test overlap since problems such as grade school math [Cobbe et al., 2021] and commonsense reasoning [Talmor et al., 2019] might be readily available in pretraining corpora, making it less convincing for evaluating reasoning abilities. On the contrary, the synthetic graph reasoning problems and their answers are highly unlikely to have exact matches in the training corpora, which makes NLGraph a more robust benchmark towards evaluating language model reasoning. 

**Fine-tuning to elicit graph reasoning abilities.** To further study the graphical thinking abilities of LLMs, we envision fine-tuning as a possible direction for future work. We plan to fine-tune language models on the chain-of-thought reasoning process towards graph-based tasks on both single- and multi-task settings to see if fine-tuning might lead to enhanced graph reasoning abilities. 

## **B Limitations** 

**Tasks in NLGraph benchmark are not complete.** While we have incorporated eight graph reasoning tasks with varying complexity in the NLGraph benchmark, there are many more important graph algorithms that test different levels of graph reasoning abilities. It might also be interesting to see how LLMs perform on other graph tasks such as finding the Eulerian path, the minimum spanning tree, and the cut-edge. 

**Language models that we evaluate are not complete.** We only consider four black-box LLMs, TEXT-DAVINCI-003, CODE-DAVINCI-002, GPT-3.5-TURBO, and GPT-4 in our experiments. Since we will make the NLGraph benchmark publicly available, we leave it to future work on evaluating the graph reasoning abilities of other open-source LLMs. 

**Limited dataset size.** Due to monetary costs, we only evaluate LLMs on the standard version of the NLGraph benchmark which has 5,902 problems throughout the paper. We believe evaluating LLMs on the extended version of the NLGraph benchmark, with 5x more problems, may bring stronger proof to the findings we present. 

**Methods for improving graph reasoning abilities.** The two prompting methods we present are simple instruction-based approaches, which work on easy graph reasoning problems to varying extents. However, on more complex graph reasoning problems, as the overall graph reasoning abilities of LLMs are limited, the instruction-based methods seem to have only marginal effects. In future work, we hope to investigate methods such as asking LLMs to generate and execute code, or simulating steps of algorithmic solutions while maintaining the state variables. 

## **C NLGraph Details** 

In Table 6, we provide the details of the NLGraph benchmark including edge probabilities and specific values of parameters mentioned in §2.2. 

14 

|**Subset**|**Connect.**|**Cycle**|**Topo. Sort**|**Shortest Path**|**Maximum Flow**|**Bipartite Graph**|**Hamilton Path**|**GNNs**|
|---|---|---|---|---|---|---|---|---|
|# EASY|_p_: 0.3, 0.7, 1.0|_m_: 1-4|_p_: 0.3, 0.5, 0.7|_p_: 0.5, 0.7, 0.9;_w_: 1-4;_ℓ_: 2-6|_p_: 0.2, 0.3;_c_: 1-10|_p_: 0.3-0.7|_p_: 0.4, 0.6|_p_: 0.4;_ℓ_: 1|
|# MEDIUM|_p_: 0.3, 0.7, 1.0|_m_: 1-4|_p_: 0.3, 0.5, 0.7|/|/|/|/|/|
|# HARD|_p_: 0.3, 0.7|_m_: 1-4|_p_: 0.3, 0.5|_p_: 0.2, 0.25;_w_: 1-10;_ℓ_: 2-6|_p_: 0.25;_c_: 1-20|_p_: 0.2-0.6|_p_: 0.4, 0.6|_p_: 0.2;_ℓ_: 1|



Table 6: Details of the NLGraph benchmark. _p_ denotes the edge probability. Other characters have the same meaning mentioned in §2.2. 

|**Method**||**S**|**hortest Path**||
|---|---|---|---|---|
||**Easy**|**Hard**|**Easy (PC)**|**Hard (PC)**|
|BAG|**67.78**|**33.50**|79.20|**42.56**|
|BAG-DOT|65.00|29.00|75.55|37.18|
|ALGORITHMIC-DOT|66.67|31.00|78.27|39.68|
|INSTRUCTION#1|66.22|32.50|78.18|40.32|
|INSTRUCTION#2|**67.78**|28.50|77.32|37.06|
|INSTRUCTION#3|**67.78**|30.50|**79.56**|37.89|



Table 7: The results of variants of instructions on the shortest path task. The BAG prompting approach achieves the best performance across three of the four settings. 

## **D Analysis** 

**Instruction variants** To further study the effect of BAG prompting and ALGORITHMIC prompting, we replace the instructions with only a sequence of dots (...) equal to the number of characters in the instruction. This is to investigate whether the improved performance is attributed to the natural language instructions or simply increased computation. We also replace the BAG prompting with three other instructions not directly related to graph problems, specifically, _Let’s think step by step_ (INSTRUCTION 1), _Examine each detail carefully_ (INSTRUCTION 2), _Think it through systematically_ (INSTRUCTION 3). As illustrated in Table 7, the BAG prompting method generally outperforms the instruction variants, indicating the effectiveness of this method. 

**Graph definition variants** We study how replacing the abstract descriptions of graphs with realworld objects would impact model performance. Specifically, for the shortest path task, we change all the "node"s into "city"s, "edge"s into "road"s, and "weight"s into "distance"s. As shown in Table 9, the model performance improves on the easy subset but drops on the hard subset. While language models are indeed sensitive to the specific instantiations of the graph description, the results are mixed as to which is easier or harder. 



<!-- Start of picture text -->
question<br>easy medium hard<br>100<br>80<br>easy 84.67 63.33 53.25<br>60 80<br>40<br>medium 62.00 52.67 49.75 60<br>20<br>0 40<br>3 4 5 6 7 8 hard 49.33 50.67 52.25<br># node<br>20<br>Acc exemplar<br><!-- End of picture text -->

Figure 6: Model performance for the shortest path task with different numbers of nodes on the shortest path. The performance steadily drops when the path length increases. 

Figure 7: Model performance for the cycle task with varied exemplar difficulty. When the in-context exemplars are based on more difficult problems, the performance becomes worse. 

15 

|**Method**||**Cycle**|||**S**|**hortest Path**||**Hamilt**|**on Path**|
|---|---|---|---|---|---|---|---|---|---|
||**Easy**|**Medium**|**Hard**|**Easy**|**Hard**|**Easy (PC)**|**Hard (PC)**|**Easy**|**Hard**|
|RANDOM|50.00|50.00|50.00|50.00|50.00|6.07|6.69|0.00|0.00|
|FEW-SHOT|58.00|50.00|49.75|39.44|28.50|55.10|37.63|36.67|7.00|
|COT|60.67|66.83|69.00|41.11|/|45.00|/|50.00|12.00|
|COT+SC|59.33|52.67|53.75|42.22|/|49.26|/|34.00|5.00|



Table 8: The results of CODE-DAVINCI-002 on the cycle, shortest path, and Hamilton path task. 

|**Method**||**S**|**hortest Path**||
|---|---|---|---|---|
||**Easy**|**Hard**|**Easy (PC)**|**Hard (PC)**|
|RANDOM|50.00|50.00|6.07|6.69|
|ZERO-SHOT|29.40|14.00|47.53|20.13|
|FEW-SHOT|41.11|20.50|58.78|29.28|
|COT|73.33|28.00|82.57|35.50|
|0-COT|6.67|2.00|65.40|51.95|
|COT+SC|72.78|27.00|83.50|35.19|



Table 9: Model performance when graph descriptions are changed into cities, roads, and distances on the shortest path task. 

**LLMs are brittle to problem scales** For the shortest path task, we study the correlation between model performance and the number of nodes on the optimal shortest path. We group problems by the shortest path length and present results in Figure 6 for the COT approach, which shows that the accuracy steadily drops when the number of nodes on the shortest path increases. While the reasoning process towards finding the shortest paths stays the same for optimal solutions with varying lengths, large language models are not robust to changes in graph scales and problem settings. 

**In-context exemplars and test difficulty** We investigate the model performance when the incontext exemplars and test difficulty vary. For the cycle task, we write chain-of-thought solutions for problems selected from the medium and hard subsets, and evaluate TEXT-DAVINCI-003 on the cycle task with the two prompts. We present the results in Figure 7. The performance drops when the exemplar difficulty increases, indicating that LLM struggles to learn from exemplars with more difficulty. 

### **Partial credit for the maximum flow task** 

We provide partial credit for the maximum flow task in Table 10. The performance generally has the same trend as the results provided in Figure 2. Though on the hard subsets, the performance of COT is the highest, we believe this is more like guessing, as when COT is combined with self-consistency, the performance drops significantly. 

|**Method**|**Easy**|**Hard**|
|---|---|---|
|ZERO-SHOT|**25.65**|10.37|
|FEW-SHOT|24.83|12.37|
|COT|16.99|**22.07**|
|0-COT|17.41|7.04|
|COT+SC|9.88|8.62|



Table 10: Partial credit for the maximum flow task. 

## **E Additional Large Language Models** 

### **E.1 CODE-DAVINCI-002 Results** 

We evaluate CODE-DAVINCI-002 on cycle, shortest path, and Hamilton path. The results are provided in Table 8. The findings are mostly similar to TEXT-DAVINCI-003: language models are preliminary graph reasoners on easy tasks while the benefit of in-context learning and advanced prompting is limited on more complex problems. However, in the COT and COT+SC settings, CODE-DAVINCI002 generates too many tokens before reaching the final answer, so we do not present the results in Table 8. 

16 

### **E.2 OPT Results** 

We fine-tune OPT-2.7B [Zhang et al., 2022b] and evaluate the model on the NLGraph benchmark. We randomly divide the standard version of the NLGraph benchmark into 4902 training problems and 1,000 test problems. We generate zero-shot solutions for the training problems, combine the solutions with the problems, and attain nine corpus of text ( _i.e._ one for each task and one that concatenating all the text). We then fine-tune OPT on the nine corpus separately. However, we find that fine-tuning did not elicit the graph reasoning abilities of OPT-2.7B: the generated text is mostly meaningless, falling short of answering questions and following formats. We leave it to future work on fine-tuning larger language models to elicit graph reasoning abilities due to our limitations in computational resources. 

### **E.3 Qualitative Analaysis with GPT-3.5-TURBO and GPT-4** 

Due to monetary costs, we only conduct qualitative analysis on GPT-3.5-TURBO and GPT-4 with 19 representative problems across the eight tasks. We provide the results in Table 11, Table 12, Table 13, Table 14, Table 15. Results demonstrate that while GPT-4 does present better graph reasoning abilities, it is still far from being a robust reasoner towards graph-based problems. 

17 

Table 11: Results of GPT-3.5-TURBO and GPT-4 on 19 cases (#1 to #6 example) through the eight tasks. We omitted the COT in-context exemplars in the table. 

|**Question**|GPT-3.5-TURBO|GPT-4|
|---|---|---|
|Determine if there is a path between two nodes in the<br>graph. Note that (i,j) means that node i and node j are<br>connected with an undirected edge. Graph: (0,4) (1,3)<br>(1,2) (1,6) (2,5) (2,6) (3,5) (5,6)<br>Q: Is there a path between node 4 and node 5?|Node 4 is not directly connected to<br>node 5, but we can follow the path:<br>4->0->6->2->5, so the answer is yes.<br>�|Node 4 is only connected to node 0,<br>which does not have any connections<br>to the other nodes in the graph. Node<br>5 is in the connected block consisting<br>of nodes 1, 2, 3, 5, and 6. Node 4 and<br>node 5 are not in the same connected<br>block, so the answer is no. �|
|Determine if there is a path between two nodes in the<br>graph. Note that (i,j) means that node i and node j<br>are connected with an undirected edge. Graph: (0,3)<br>(0,5) (0,11) (0,8) (0,6) (0,1) (1,10) (1,3) (1,5) (1,9) (1,6)<br>(1,2) (2,10) (2,3) (2,5) (2,9) (2,8) (2,7) (2,6) (2,13) (3,9)<br>(3,11) (3,8) (3,7) (4,12) (5,10) (5,9) (5,8) (5,7) (5,6)<br>(6,10) (6,9) (6,11) (6,8) (7,10) (7,11) (7,8) (7,13) (8,10)<br>(8,11) (8,13) (9,10) (9,11) (9,13) (10,11) (10,13)<br>Q: Is there a path between node 6 and node 3?|Node 6 is connected to node 0, node<br>0 is connected to node 3. We can fol-<br>low the path: 6->0->3, so the answer<br>is yes. �|A: Node 6 is connected to node 2,<br>node 2 is connected to node 3. We<br>can follow the path: 6->2->3, so the<br>answer is yes. �|
|In an undirected graph, (i,j) means that node i and node<br>j are connected with an undirected edge. The nodes are<br>numbered from 0 to 7, and the edges are: (2,4) (0,3)<br>(1,2) (5,7) (1,5) (6,5) (1,0)<br>Q: Is there a cycle in this graph?|The edges (1,2), (2,4), (4,0), (0,3),<br>(3,1) form a cycle, so yes, there is a<br>cycle in this graph. �|The edges (1,0), (1,2), (1,5), (6,5),<br>(5,7) do not form a cycle. However,<br>the edges (1,0), (1,2), (2,4) do form a<br>cycle. So yes, there is a cycle in this<br>graph. �|
|In an undirected graph, (i,j) means that node i and node<br>j are connected with an undirected edge. The nodes are<br>numbered from 0 to 7, and the edges are: (1,7) (0,6)<br>(1,3) (4,5) (1,0) (0,4) (0,2) (7,2)<br>Q: Is there a cycle in this graph?|The edges (0,6), (6,4), (4,5), (5,7),<br>(7,1), (1,0) form a cycle, so yes, there<br>is a cycle in this graph. �|The edges (1,7), (7,2), (2,0), (0,1)<br>form a cycle, so yes, there is a cycle<br>in this graph. �|
|In an undirected graph, the nodes are numbered from 0<br>to 5, and the edges are: An edge between node 2 and<br>node 0 with weight 2, An edge between node 0 and<br>node 4 with weight 1, An edge between node 1 and<br>node 2 with weight 4, An edge between node 1 and<br>node 3 with weight 4, An edge between node 4 and<br>node 1 with weight 4, An edge between node 2 and<br>node 3 with weight 1, An edge between node 2 and<br>node 5 with weight 2, An edge between node 2 and<br>node 4 with weight 3, An edge between node 5 and<br>node 3 with weight 2, An edge between node 3 and<br>node 4 with weight 3, An edge between node 4 and<br>node 5 with weight 2.<br>Q: Give the shortest path from node 3 to node 0.|All the paths from node 3 to node 0<br>are: 3,2,0 with a total weight of 2 +<br>2 = 4, 3,2,4,1,0 with a total weight<br>of 3 + 4 + 1 = 8, 3,2,4,0 with a total<br>weight of 3 + 1 = 4, 3,1,4,0 with a<br>total weight of 4 + 4 + 1 = 9, 3,1,2,0<br>with a total weight of 4 + 4 + 2 = 10,<br>3,5,2,0 with a total weight of 2 + 2<br>+ 2 = 6, 3,5,4,0 with a total weight<br>of 2 + 2 + 1 = 5. The weight of path<br>3,2,0 and 3,5,4,0 is the smallest, so<br>the shortest path from node 3 to node<br>0 is either 3,2,0 or 3,5,4,0, both with<br>a total weight of 4. �|All the paths from node 3 to node<br>0 are: 3,2,0 with a total weight of 1<br>+ 2 = 3, 3,1,2,0 with a total weight<br>of 4 + 4 + 2 = 10, 3,4,0 with a total<br>weight of 3 + 1 = 4, 3,4,2,0 with a<br>total weight of 3 + 3 + 2 = 8, 3,5,2,0<br>with a total weight of 2 + 2 + 2 = 6,<br>3,5,4,0 with a total weight of 2 + 2 +<br>1 = 5.<br>The weight of path 3,2,0 is the small-<br>est, so the shortest path from node 3<br>to node 0 is 3,2,0 with a total weight<br>of 3. �|
|In an undirected graph, the nodes are numbered from 0<br>to 4, and the edges are: An edge between node 1 and<br>node 0 with weight 1, An edge between node 2 and<br>node 0 with weight 1, An edge between node 4 and<br>node 1 with weight 1, An edge between node 1 and<br>node 2 with weight 3, An edge between node 2 and<br>node 3 with weight 3.<br>Q: Give the shortest path from node 3 to node 1.|All the paths from node 3 to node 1<br>are: 3,2,1 with a total weight of 3<br>+ 3 = 6, 3,2,0,1 with a total weight<br>of 1 + 1 + 1 = 3, 3,2,1,0,1 with a<br>total weight of 3 + 1 + 1 + 1 = 6,<br>3,2,0,1,4,1 with a total weight of 1 +<br>1 + 1 + 1 + 1 = 5. The weight of path<br>3,2,0,1 is the smallest, so the shortest<br>path from node 3 to node 1 is 3,2,0,1<br>with a total weight of 3. �|All the paths from node 3 to node 1<br>are: 3,2,1 with a total weight of 3 +<br>3 = 6, 3,2,0,1 with a total weight of<br>3 + 1 + 1 = 5.<br>The weight of path 3,2,0,1 is the<br>smallest, so the shortest path from<br>node 3 to node 1 is 3,2,0,1 with a to-<br>tal weight of 5. �|



18 

Table 12: Results of GPT-3.5-TURBO and GPT-4 on 19 cases (#7 to #9 example ) through the eight tasks. We omitted the COT in-context exemplars in the table. 

|**Question**|GPT-3.5-TURBO|GPT-4|
|---|---|---|
|In an undirected graph, the nodes are numbered from 0|All the paths from node 2 to node 3|All the paths from node 2 to node 3|
|to 6, and the edges are: An edge between node 0 and<br>|are: 2,0,3 with a total weight of 1 +<br>|are: 2,0,3 with a total weight of 1 + 4<br>|
|node 2 with weight 1, An edge between node 3 and<br>|4 = 5, 2,1,3 with a total weight of 2<br>|= 5, 2,1,3 with a total weight of 2 + 3<br>|
|node 0 with weight 4, An edge between node 5 and|+ 3 = 5, 2,4,3 with a total weight of|= 5, 2,1,0,3 with a total weight of 2 +|
|node 0 with weight 2, An edge between node 4 and<br>|3 + 2 = 5. The weight of path 2,0,3<br>|4 + 4 = 10, 2,1,6,3 with a total weight<br>|
|node 0 with weight 3, An edge between node 0 and|is the smallest, so the shortest path|of 2 + 2 + 4 = 8, 2,4,3 with a total|
|node 1 with weight 4, An edge between node 0 and<br>|from node 2 to node 3 is 2,0,3 with a<br>|weight of 3 + 2 = 5, 2,4,0,3 with a<br>|
|node 6 with weight 2, An edge between node 2 and<br>|total weight of 5. �|total weight of 3 + 3 + 4 = 10, 2,4,1,3<br>|
|node 1 with weight 2, An edge between node 3 and||with a total weight of 3 + 3 + 3 = 9,|
|node 1 with weight 3, An edge between node 4 and||<br>2,4,1,0,3 with a total weight of 3 +|
|node 1 with weight 3, An edge between node 1 and||3 + 4 + 4 = 14, 2,4,1,6,3 with a total|
|node 6 with weight 2, An edge between node 2 and||weight of 3 + 3 + 2 + 4 = 12, 2,5,0,3|
|node 5 with weight 4, An edge between node 2 and||with a total weight of 4 + 2 + 4 = 10,|
|node 4 with weight 3, An edge between node 6 and<br>||2,5,4,3 with a total weight of 4 + 5 +<br>|
|node 2 with weight 2, An edge between node 3 and||2 = 11, 2,5,4,0,3 with a total weight|
|node 5 with weight 1, An edge between node 4 and||of 4 + 5 + 3 + 4 = 16, 2,5,4,1,3 with|
|node 3 with weight 2, An edge between node 3 and<br>||a total weight of 4 + 5 + 3 + 3 = 15,<br>|
|node 6 with weight 4, An edge between node 4 and||2,5,6,3 with a total weight of 4 + 6|
|node 5 with weight 3, An edge between node 4 and||+ 4 = 14, 2,6,1,3 with a total weight|
|node 6 with weight 1, An edge between node 6 and||of 2 + 2 + 3 = 7, 2,6,1,0,3 with a|
|node 5 with weight 2.||total weight of 2 + 2 + 4 + 4 = 12,|
|Q: Give the shortest path from node 2 to node 3.||2,6,5,0,3 with a total weight of 2 +<br>5 + 2 + 4 = 13, 2,6,5,4,3 with a total<br>weight of 2 + 5 + 5 + 2 = 14.<br>The weight of paths 2,0,3, 2,1,3, and<br>2,4,3 is the smallest. So, there are<br>three shortest paths from node 2 to<br>node 3, which are 2,0,3; 2,1,3; and<br>2,4,3, each with a total weight of 5.<br>�|
|In a directed graph with 5 nodes numbered from 0 to 4:|This is not possible as there is a cycle|Since no nodes are required to be vis-|
|node 2 should be visited before node 4<br>|between nodes 0, 1, and 4. Node 2<br>|ited before node 2 and node 3, node 2<br>i|
|node 2 should be visited before node 1|cannot be visited before nodes 0, 1,|and node 3 can be visited first. Since|
|node 2 should be visited before node 0|and 4, and nodes 0, 1, and 4 cannot|visiting node 4 requires visiting node|
|node 4 should be visited before node 1|be visited before node 2.Therefore|2 first after node 2 is visited node 4|
|<br>node 4 should be visited before node 0|,<br>it is not possible to visit all the nodes|i,     ,<br>can be visited. Since visiting node 0|
|Q: Can all the nodes be visited? Give the solution.|<br>in this graph. �|<br>requires visiting node 2, node 4 first,<br>after node 2 and node 4 are visited,<br>node 0 can be visited. Since visiting<br>node 1 requires visiting node 2, node<br>4 first, after node 2 and node 4 are<br>visited, node 1 can be visited. So the<br>solution is: 2,3,4,0,1. �|
|In a directed graph with 5 nodes numbered from 0 to 4:<br>node 0 should be visited before node 1<br>d 1 hld b iitd bf d 2|This graph has a cycle, which means<br>it is not possible to visit all nodes in<br>liddSifillthi|Since no nodes are required to be vis-<br>ited before node 4, node 4 can be<br>iitdfitSiiitid0|
|noe  sou e vse eore noe|a va orer. pecicay, ere s|vse irs. nce vsng noe|
|node 3 should be visited before node 1|acyclebetweennodes12and3|and node 3 requires visiting node 4|
|<br>node 3 should be visited before node 2|, ,  ,<br>which cannot be resolved based on<br>|<br>first, after node 4 is visited, node 0|
|node 4 should be visited before node 3|the given constraints. �|i<br>and node 3 can be visited. Since vis-|
|node 4 should be visited before node 0<br>node 4 should be visited before node 1||iting node 1 requires visiting node<br>0 and node 3 first, after node 0 and|
|Q: Can all the nodes be visited? Give the solution.||i<br>node 3 are visited, node 1 can be vis-<br>ited. Since visiting node 2 requires<br>visiting node 1 and node 3 first, after<br>node 1 and node 3 are visited, node<br>2 can be visited. So the solution is:<br>4,0,3,1,2. �|



19 

Table 13: Results of GPT-3.5-TURBO and GPT-4 on 19 cases (#10 to #12 example ) through the eight tasks. We omitted the COT in-context exemplars in the table. 

|**Question**|GPT-3.5-TURBO|GPT-4|
|---|---|---|
|In a directed graph with 6 nodes numbered from 0 to 5:<br>node 0 should be visited before node 5<br>node 0 should be visited before node 1<br>node 2 should be visited before node 1<br>node 3 should be visited before node 0<br>node 3 should be visited before node 5<br>node 3 should be visited before node 1<br>node 4 should be visited before node 0<br>node 4 should be visited before node 2<br>node 5 should be visited before node 2<br>Q: Can all the nodes be visited? Give the solution|Since no nodes are required to be vis-<br>ited before node 3 and node 4, node 3<br>and node 4 can be visited first. Since<br>visiting node 0 requires visiting node<br>3 first, after node 3 is visited, node 0<br>can be visited. Since visiting node 1<br>requires visiting node 0, node 2, node<br>3 first, after node 0, node 2, and node<br>3 are visited, node 1 can be visited.<br>Since visiting node 5 requires visit-<br>ing node 0, node 3 first, after node<br>0 and node 3 are visited, node 5 can<br>be visited. Since visiting node 2 re-<br>quires visiting node 4, node 5 first,<br>after node 4 and node 5 are visited,<br>node 2 can be visited. So the solution<br>is: 3,4,0,2,1,5. �|Since no nodes are required to be vis-<br>ited before node 3 and node 4, node 3<br>and node 4 can be visited first. Since<br>visiting node 0 requires visiting node<br>3 and node 4 first, after node 3 and<br>node 4 are visited, node 0 can be vis-<br>ited. Since visiting node 5 requires<br>visiting node 0 and node 3 first, after<br>node 0 and node 3 are visited, node 5<br>can be visited. Since visiting node 1<br>requires visiting node 0, node 2, and<br>node 3 first, node 2 must be visited<br>before node 1. Since visiting node<br>2 requires visiting node 4 and node<br>5 first, after node 4 and node 5 are<br>visited, node 2 can be visited. Now,<br>since node 0, node 2, and node 3<br>have been visited, node 1 can be vis-<br>ited. So the solution is: 3,4,0,5,2,1.<br>�|
|In a directed graph, the nodes are numbered from 0 to<br>5, and the edges are: an edge from node 1 to node 3<br>with capacity 4,<br>an edge from node 1 to node 0 with capacity 9,<br>an edge from node 2 to node 1 with capacity 4,<br>an edge from node 3 to node 1 with capacity 4,<br>an edge from node 4 to node 3 with capacity 1,<br>an edge from node 4 to node 5 with capacity 2,<br>an edge from node 5 to node 1 with capacity 4,<br>an edge from node 5 to node 0 with capacity 7.<br>Q: What is the maximum flow from node 4 to node 0?|There is no path from node 4 to node<br>0, so the maximum flow from node<br>4 to node 0 is 0. �|From the source (node 4), we can<br>send 1 unit of flow to node 3, and 2<br>units of flow to node 5.<br>1 unit of flow arrives at node 3, then<br>we can send 1 unit of flow from node<br>3 to node 1.<br>2 units of flow arrive at node 5, then<br>we can send 2 units of flow from<br>node 5 to node 0.<br>1 unit of flow arrives at node 1, then<br>we can send 1 unit of flow from node<br>1 to node 0.<br>The total unit of flow arrives at node<br>0 is 3. So the maximum flow from<br>node 4 to node 0 is 3. �|
|In a directed graph, the nodes are numbered from 0 to<br>7, and the edges are: an edge from node 0 to node 6<br>with capacity 1,<br>an edge from node 0 to node 7 with capacity 10,<br>an edge from node 2 to node 1 with capacity 9,<br>an edge from node 2 to node 7 with capacity 8,<br>an edge from node 3 to node 1 with capacity 9,<br>an edge from node 3 to node 6 with capacity 10,<br>an edge from node 3 to node 4 with capacity 7,<br>an edge from node 4 to node 6 with capacity 1,<br>an edge from node 5 to node 3 with capacity 7,<br>an edge from node 5 to node 2 with capacity 9,<br>an edge from node 6 to node 4 with capacity 1,<br>an edge from node 7 to node 5 with capacity 8,<br>an edge from node 7 to node 6 with capacity 5.<br>Q: What is the maximum flow from node 2 to node 4?|From the source (node 2), we can<br>send 8 units of flow to node 7, and 9<br>units of flow to node 1.<br>8 units of flow arrive at node 7, then<br>we can send 5 units of flow from<br>node 7 to node 6, and 3 units of flow<br>from node 7 to node 5.<br>9 units of flow arrive at node 1, then<br>we can send 9 units of flow from<br>node 3 to node 1.<br>9 units of flow arrive at node 6, then<br>we can send 1 unit of flow from node<br>6 to node 4.<br>7 units of flow arrive at node 3, then<br>we can send 7 units of flow from<br>node 3 to node 4.<br>The total unit of flow arrives at node<br>4 is 8. So the maximum flow from<br>node 2 to node 4 is 8. �|From the source (node 2), we can<br>send 9 units of flow to node 1, and 8<br>units of flow to node 7.<br>9 units of flow arrive at node 1, then<br>we can send 9 units of flow from<br>node 1 to node 3.<br>8 units of flow arrive at node 7, then<br>we can send 8 units of flow from<br>node 7 to node 5, and 5 units of flow<br>from node 7 to node 6.<br>8 units of flow arrive at node 5, then<br>we can send 7 units of flow from<br>node 5 to node 3, and 1 unit of flow<br>from node 5 to node 2.<br>14 units of flow arrive at node 3, then<br>we can send 14 units of flow from<br>node 3 to node 4.<br>The total unit of flow arrives at node<br>4 is 14. So the maximum flow from<br>node 2 to node 4 is 14. �|



20 

Table 14: Results of GPT-3.5-TURBO and GPT-4 on 19 cases (#13 to #16 example ) through the eight tasks. We omitted the COT in-context exemplars in the table. 

|**Question**|GPT-3.5-TURBO|GPT-4|
|---|---|---|
|In a directed graph, the nodes are numbered from 0 to<br>7, and the edges are: an edge from node 0 to node 6<br>with capacity 9,<br>d f d 0 t d 3 ith it 7|There is no path from node 1 to node<br>6 in this graph, so the maximum flow<br>from node 1 to node 6 is 0. �|From the source (node 1), we can<br>send 8 units of flow to node 7, and<br>3 units of flow to node 2. 8 units of<br>flitd7th|
|an ege rom noe  o noe  w capacy ,<br>an edge from node 1 to node 7 with capacity 8,<br>an ede from node 1 to node 2 with caacit 3||low arrve a noe , en we can<br>send 4 units of flow from node 7 to<br>node 4 and 4 units of flow from node|
|g        py ,<br>an edge from node 2 to node 7 with capacity 7,||,     l<br>7 to node 1. 4 units of flow arrive at|
|<br>an edge from node 2 to node 4 with capacity 5,<br>||l<br>node 4, then we can send 3 units of<br>l|
|an edge from node 3 to node 5 with capacity 7,<br>an edge from node 3 to node 1 with capacity 8,<br>d f d 4 t d 0 ith it 3||flow from node 4 to node 0. 3 units<br>of flow arrive at node 0, then we can<br>d 3 it f fl f d 0 t|
|an ege rom noe  o noe  w capacy ,<br>||sen  uns o low rom noe  o<br> l|
|an edge from node 5 to node 7 with capacity 5,<br>an edge from node 6 to node 5 with capacity 6,<br>||node 6. 3 units of flow arrive at node<br>2, then we can send 3 units of flow<br>|
|an edge from node 6 to node 7 with capacity 6,||from node 2 to node 4. 3 units of|
|an edge from node 6 to node 0 with capacity 9,<br>an edge from node 7 to node 4 with capacity 4,<br>an edge from node 7 to node 1 with capacity 8.<br>Q: What is the maximum flow from node 1 to node 6?||flow arrive at node 4, then we can<br>send 3 units of flow from node 4 to<br>node 0. 3 units of flow arrive at node<br>0, then we can send 3 units of flow<br>from node 0 to node 6.<br>The total unit of flow arrives at node<br>6 is 6. So the maximum flow from<br>node 1 to node 6 is 6. �|
|In an undirected graph, (i,j) means that node i and node<br>j are connected with an undirected edge. The nodes are<br>numbered from 0 to 6, and the edges are: (4,3) (6,5)<br>(5,1) (3,0) (2,4) (1,0) (5,2) (4,0) (2,3) (0,2) (6,2)<br>Q: Is there a path in this graph that visits every node<br>exactly once? If yes, give the path. Note that in a path,<br>adjacent nodes must be connected with edges.|No, there is no path that visits every<br>node exactly once. This graph con-<br>tains two disconnected components:<br>0,1,2,3,4 and 5,6. It is not possible<br>to visit all nodes in a single path be-<br>cause there is no edge connecting the<br>two components. �|Yes. We can start at node 3. As node<br>3 is connected with node 0, and node<br>0 is not visited, we can then visit<br>node 0. As node 0 is connected with<br>node 1, and node 1 is not visited, we<br>can then visit node 1. As node 1 is<br>connected with node 5, and node 5 is<br>not visited, we can then visit node 5.<br>As node 5 is connected with node 6,<br>and node 6 is not visited, we can then<br>visit node 6. As node 6 is connected<br>with node 2, and node 2 is not visited,<br>we can then visit node 2. As node 2<br>is connected with node 4, and node 4<br>is not visited, we can then visit node<br>4. The path can be: 3, 0, 1, 5, 6, 2, 4.<br>�|
|In an undirected graph, (i,j) means that node i and node<br>j are connected with an undirected edge. The nodes are<br>numbered from 0 to 4, and the edges are: (1,3) (1,2)<br>(4,3) (2,0) (0,4) (0,1)|No, there is no path in this graph that<br>visits every node exactly once. This<br>is because node 1 has degree 2, mean-<br>ing it is connected to two other nodes.|Yes. We can start at node 0. As node<br>0 is connected with node 1, and node<br>1 is not visited, we can then visit<br>node 1. As node 1 is connected with|
|<br>Q: Is there a path in this graph that visits every node<br>exactly once? If yes, give the path. Note that in a path,<br>adjacent nodes must be connected with edges.|<br>In order to visit every node exactly<br>once, we would need to start and end<br>at node 1, but once we leave node 1,<br>we cannot return to it without visit-<br>ing another node twice. Therefore, it<br>is impossible to find a path that visits<br>every node exactly once in this graph.<br>�|node 3, and node 3 is not visited, we<br>can then visit node 3. As node 3 is<br>connected with node 4, and node 4<br>is not visited, we can then visit node<br>4. As node 4 is connected with node<br>2, and node 2 is not visited, we can<br>then visit node 2. The path can be:<br>0,1,3,4,2. �|
|There are 4 job applicants numbered from 0 to 3, and 2<br>jobs numbered from 0 to 1Each applicant is interested|Applicant 0 is interested in job 0, job<br>1|Applicant 0 is interested in job 0, job<br>1|
|.  <br>in some of the jobs. Each job can only accept one<br>applicant and a job applicant can be appointed for only<br>b|.<br>Applicant 1 is interested in job 0.<br>Applicant 2 is interested in job 0, job<br>1|.<br>Applicant 1 is interested in job 0.<br>Applicant 2 is interested in job 0, job<br>1|
|one jo.<br>Applicant 0 is interested in job 1.<br>Alicant 2 is interested in job 0|.<br>Applicant 3 is interested in job 0, job<br>1|.<br>Applicant 3 is interested in job 0, job<br>1|
|pp      .<br>Applicant 0 is interested in job 0.|.<br>We can make the following assign-|.<br>We can make the following assign-|
|Applicant 2 is interested in job 1.<br>|ments:<br>|ments:<br>|
|Applicant 3 is interested in job 1.<br>Applicant 3 is interested in job 0.<br>Ali 1 i id i b 0|applicant 0: job 1<br>applicant 2: job 0<br>li 3b 1|applicant 0: job 0<br>applicant 1: - (no job available)<br>li 2b 1|
|ppcant  s ntereste n jo .<br>Q: Find an assignment of jobs to applicants in such that<br>the maximum number of applicants find the job they<br>are interested in.|appcant : jo<br>3 applicants can find the job they are<br>interested in. �|appcant : jo<br>applicant 3: - (no job available)<br>2 applicants can find the job they are<br>interested in. �|



21 

Table 15: Results of GPT-3.5-TURBO and GPT-4 on 19 cases (#17 to #19 example ) through the eight tasks. We omitted the COT in-context exemplars in the table. 

|**Question**|GPT-3.5-TURBO|GPT-4|
|---|---|---|
|There are 5 job applicants numbered from 0 to 4, and 6<br>jobs numbered from 0 to 5. Each applicant is interested<br>in some of the jobs. Each job can only accept one<br>applicant and a job applicant can be appointed for only<br>one job.<br>Applicant 0 is interested in job 3.<br>Applicant 4 is interested in job 5. Applicant 4 is inter-<br>ested in job 4.<br>Applicant 3 is interested in job 0.<br>Applicant 0 is interested in job 5.<br>Applicant 1 is interested in job 0.<br>Applicant 0 is interested in job 2.<br>Applicant 0 is interested in job 4.<br>Applicant 4 is interested in job 0.<br>Applicant 4 is interested in job 2.<br>Applicant 2 is interested in job 3.<br>Q: Find an assignment of jobs to applicants in such that<br>the maximum number of applicants find the job they<br>are interested in.|Applicant 0 is interested in job 2, job<br>3, job 4, job 5. Applicant 1 is inter-<br>ested in job 0. Applicant 2 is inter-<br>ested in job 3. Applicant 3 is inter-<br>ested in job 0. Applicant 4 is inter-<br>ested in job 0, job 2, job 4, job 5. We<br>can make the following assignments:<br>applicant 0: job 5 applicant 1: job 0<br>applicant 2: job 3 applicant 3: job 0<br>applicant 4: job 2 5 applicants can<br>find the job they are interested in. �|Applicant 0 is interested in job 2, job<br>3, job 4, job 5. Applicant 1 is inter-<br>ested in job 0. Applicant 2 is inter-<br>ested in job 3. Applicant 3 is inter-<br>ested in job 0. Applicant 4 is inter-<br>ested in job 0, job 2, job 4, job 5. We<br>can make the following assignments:<br>applicant 0: job 3 applicant 1: job 0<br>applicant 4: job 4 3 applicants can<br>find the job they are interested in. �|
|n an undirected graph, the nodes are numbered from<br>0 to 5, and every node has an embedding. (i,j) means<br>that node i and node j are connected with an undirected<br>edge.<br>Embeddings:<br>node 0: [1,1]<br>node 1: [0,1]<br>node 2: [1,0]|Layer 1: node 0: sum of embeddings<br>of node 1, node 5, [0,1] + [0,1] =<br>[0,2].<br>node 1: sum of embeddings of node<br>0, node 4, node 5, [1,1] + [0,0] +<br>[0,1] = [1,2].<br>node 2: sum of embeddings of node<br>4, [0,0] = [0,0].|Layer 1:<br>node 0: sum of embeddings of node<br>1, node 5, [0,1] + [0,1] = [0,2].<br>node 1: sum of embeddings of node<br>0, node 4, node 5, [1,1] + [0,0] +<br>[0,1] = [1,2].<br>node 2: sum of embeddings of node<br>4, [0,0] = [0,0].|
|node 3: [1,1]|node 3: sum of embeddings of node|node 3: sum of embeddings of node|
|node 4: [0,0]<br>|<br>4, [0,0] = [0,0].<br>|<br>4, [0,0] = [0,0].<br>|
|node 5: [0,1]<br>The edges are: (0,1) (5,0) (1,4) (1,5) (2,4) (4,3)<br>In a simple graph convolution layer, each node’s em-<br>bedding is updated by the sum of its neighbors’ embed-<br>dings.<br>Q: What’s the embedding of each node after one layer<br>of simple graph convolution layer?|node 4: sum of embeddings of node<br>1, node 2, node 3, [1,2] + [1,0] + [0,0]<br>= [2,2].<br>node 5: sum of embeddings of node<br>0, node 1, [0,2] + [1,2] = [1,4].<br>So the answer is:<br>node 0: [0,2]<br>node 1: [1,2]<br>node 2: [0,0]<br>node 3: [0,0]<br>|node 4: sum of embeddings of node<br>1, node 2, node 3, [0,1] + [1,0] + [1,1]<br>= [2,2].<br>node 5: sum of embeddings of node<br>0, node 1, [1,1] + [0,1] = [1,2].<br>So the answer is:<br>node 0: [0,2]<br>node 1: [1,2]<br>node 2: [0,0]<br>node 3: [0,0]<br>|
||node 4: [2,2]<br>node 5: [1,4]�|node 4: [2,2]<br>node 5: [1,2]�|
|In an undirected graph, the nodes are numbered from<br>0 to 7, and every node has an embedding. (i,j) means<br>that node i and node j are connected with an undirected<br>edge.<br>Embeddins:|Layer 1: node 0: sum of embeddings<br>of node 3, node 4, node 6, [1,1] +<br>[1,1] + [1,0] = [3,2].<br>node 1: sum of embeddings of node<br>4 [11] = [11]|Layer 1: node 0: sum of embeddings<br>of node 3, node 4, node 6, [1,1] +<br>[1,1] + [1,0] = [3,2].<br>node 1: sum of embeddings of node<br>5 node 4 [00] + [11] = [11]|
|g<br>node 0: [0,1]<br>node 1: [1,1]<br>node 2: [1,0]<br>|, ,  ,.<br>node 2: sum of embeddings of node<br>3, node 5, node 6, [1,1] + [0,0] +<br>[1,0] = [2,1].<br>|,  , ,  ,  ,.<br>node 2: sum of embeddings of node<br>5, node 3, node 6, [0,0] + [1,1] +<br>[1,0] = [2,1].<br>|
|node 3: [1,1]<br>node 4: [1,1]<br>node 5: [0,0]<br>node 6: [1,0]<br>node 7: [1,0]<br>The edges are: (0,3) (4,0) (6,0) (5,1) (1,4) (5,2) (2,3)<br>(2,6) (3,5) (3,6) (5,4) (7,5)<br>In a simple graph convolution layer, each node’s em-<br>bedding is updated by the sum of its neighbors’ embed-<br>di|node 3: sum of embeddings of node<br>0, node 2, node 5, node 6, [0,1] +<br>[1,1] + [0,0] + [1,0] = [2,2].<br>node 4: sum of embeddings of node<br>0, node 1, node 5, [3,2] + [1,1] +<br>[0,0] = [4,3].<br>node 5: sum of embeddings of node<br>2, node 3, node 4, node 7, [2,1] +<br>[2,2] + [4,3] + [1,0] = [9,6].<br>d 6f bddi f d|node 3: sum of embeddings of node<br>0, node 2, node 5, node 6, [0,1] +<br>[1,0] + [0,0] + [1,0] = [2,1].<br>node 4: sum of embeddings of node<br>0, node 1, node 5, [0,1] + [1,1] +<br>[0,0] = [1,2].<br>node 5: sum of embeddings of node<br>1, node 2, node 3, node 4, node 7,<br>[1,1] + [1,0] + [1,1] + [1,1] + [1,0] =<br>[53]|
|ngs.<br>Q: What’s the embedding of each node after one layer<br>of simple graph convolution layer?|noe : sum o emengs o noe<br>0, node 2, node 3, [3,2] + [1,1] +<br>[1,0] = [5,3].<br>node 7: sum of embeddings of node<br>5, [9,6] = [9,6].<br>So the answer is:<br>node 0: [3,2]<br>node 1: [1,1]<br>node 2: [2,1]<br>node 3: [2,2]<br>d 443|,.<br>node 6: sum of embeddings of node<br>0, node 2, node 3, node 7, [0,1] +<br>[1,0] + [1,1] + [1,0] = [3,2].<br>node 7: sum of embeddings of node<br>5, [0,0] = [0,0].<br>So the answer is:<br>node 0: [3,2]<br>node 1: [1,1]<br>node 2: [2,1]<br>d 321|
||noe : [,]<br>node 5: [9,6]|noe : [,]<br>node 4: [1,2]|
||node 6: [5,3]<br> �|node 5: [5,3]<br>d 632|
||node 7: [9,6]|noe : [,]<br>node 7: [0,0]�|



22 

