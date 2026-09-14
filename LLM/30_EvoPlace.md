# Evolution of Optimization Algorithms for Global Placement via Large Language Models 

Xufeng Yao<sup>1</sup> , Jiaxi Jiang<sup>1</sup> , Yuxuan Zhao<sup>1</sup> , Peiyu Liao<sup>1</sup> , Yibo Lin<sup>2</sup> , Bei Yu<sup>1</sup> 

**_Abstract_ —Optimization algorithms are widely employed to tackle complex problems, but designing them manually is often labor-intensive and requires significant expertise. Global placement is a fundamental step in electronic design automation (EDA). While analytical approaches represent the state-of-the-art (SOTA) in global placement, their core optimization algorithms remain heavily dependent on heuristics and customized components, such as initialization strategies, preconditioning methods, and line search techniques. This paper presents an automated framework that leverages large language models (LLM) to evolve optimization algorithms for global placement. We first generate diverse candidate algorithms using LLM through carefully crafted prompts. Then we introduce an LLM-based genetic flow to evolve selected candidate algorithms. The discovered optimization algorithms exhibit substantial performance improvements across many benchmarks. Specifically, Our design-case-specific discovered algorithms achieve average HPWL improvements of 5.05%, 5.29% and 8.30% on MMS, ISPD2005 and ISPD2019 benchmarks, and up to 17% improvements on individual cases. Additionally, the discovered algorithms demonstrate good generalization ability and are complementary to existing parametertuning methods.** 

## I. INTRODUCTION 

Global placement is a crucial step in VLSI physical design and significantly impacts the circuit performance. Previous solutions rely on heuristic methods such as partitioning [1], simulated annealing [2] and min-cut [3] as base algorithms to minimize wirelength. Quadratic approaches [4]–[6] approximate wirelength and density using quadratic functions. Analytical placement is the current SOTA for VLSI placement [7]–[12]. Analogy to deep learning, analytical placement has two important components: optimization algorithms and differentiable objective models. The task is to minimize the objective, i.e., wirelength model [13]–[19], via moving cell locations. The cell locations are optimized via the gradients of the objective which is largely dependent on optimization algorithms. 

Due to complexity of the problem, existing optimization algorithms in placement engine remains highly heuristic and customized, including heuristic initialization, customized preconditioning methods and tailored line search techniques. Initialization strategies determine the initial positions of macros and cells, which significantly impact the final optimization results. Previous solutions [8], [10] formulate quadratic functions and solve it to determine initial placements. Later DREAMPlace [10] shows that random initialization can obtain 

This work is supported in part by The Research Grants Council of Hong Kong SAR (Project No. CUHK14208021). 

The authors are with The Chinese University of Hong Kong<sup>1</sup> , Hong Kong SAR. Peking University<sup>2</sup> . 



<!-- Start of picture text -->
64.63 HPWL Placement  Algo Code<br>Engine self.init_pos[0:placedb.num_movable_nodes] = np.random.normal(<br>    loc=(placedb.xl * 1.0 + placedb.xh *<br>Retrieve 1.0) / 2,<br> Prompt  Generate We omit following parts to save area<br>LLM<br>59.80 # Advanced Cluster-based Initialization<br>Original Algo New Algo if params.global_place_flag and params.random_center_init_flag:<br>  cluster_factor =<br>Init Algo  Merged  int(np.sqrt(num_movable_nodes / 150)) + 1<br>Evo 58.69 In   node_clusters = np.random.randint(0, cluster_factor, num_movable_nodes)<br>Prec Algo 57.57 HPWL   for cluster_id in range(cluster_factor):    idx = np.where(node_clusters ==<br>Evo Opt AlgoEvo Lower is better cluster_id)[0]    cluster_center_x = np.random.uniform(placedb.xl, placedb.xh) # Net-weight-informed noise addition<br># Iterative Refinement with Early<br>1 2 3 4 5 6 (10 3 ) CoolingWe omit these implementations and<br>Number of generations following parts to save area<br>HPWL (Obejctive)<br><!-- End of picture text -->

Fig. 1 Evolution of Optimization Algorithms 

competitive results with much shorter initialization time. As a result, it provides a heuristic that moving all cells to the center of the layout. Despite this, macro initialization remains challenging due to its greater influence on the final results. SkyPlace [20] proposes macro-aware clustering and semidefinite programming relaxation for placement initialization, which consumes longer running time overhead due to the SDP solver cost. Preconditioning is another critical part in optimization algorithms [4], [10], [21], which usually aims at solving the inverse matrix of the Hessian matrix for optimization. For instance, ePlace [10] approximates the inverse of Hessian matrix using vertex and net degrees in nonlinear optimization. Lastly, gradient-based optimizers form the foundation of analytical approaches, often with customized components. For instance, DREAMPlace families [22]–[26] introduces a Barzilai-Borwein method enabled Nesterov algorithm, and other heuristics include noise injection at high overflow plateaus and placement termination based on divergence checks. Overall, designing algorithm remains challenging due to the NP-hard nature of the problem [27]. 

**Key Motivation:** Large language models (LLM) have shown great potential in many areas [28]–[36]. In the field of automatic algorithm design, recent works [37], [38] have shown that LLMs can evolve algorithms tailored to specific combinatorial optimization problems [39]. The key motivation is to leverage the advanced capacity of LLM to comprehend the problem, provide various heuristic ideas, implement these ideas into code and improve the existing algorithm code via execution feedback. Given their remarkable performance, a key question arises: **Can LLM improve existing optimization algorithms for global placement?** Nevertheless, current works mainly addresses small-scale optimization problems, leaving industry challenges, like placement, largely unexplored. 

To address this challenge, this paper presents an automated 



<!-- Start of picture text -->
# x position init, move to center of layout<br>self.init_pos[0:placedb.num_movable_nodes] = np.random.normal(<br>    loc=(placedb.xl * 1.0 + placedb.xh * 1.0) /<br>2,scale=(placedb.xh - placedb.xl) * 0.001,<br># y position init, move to center of layout (same as x position)<br>Similar to x position, we omit implementations here to save area<br>(a) DREAMPlace Implementation<br># Adaptive Density Scaling; omit implementation here<br># Calculate layout center; omit implementation here<br># Adaptively scale x, y positions; omit implementation here<br># Advanced Cluster-based Initialization<br>if params.global_place_flag and params.random_center_init_flag:<br>  cluster_factor = int(np.sqrt(num_movable_nodes / 150)) + 1<br>  node_clusters = np.random.randint(0, cluster_factor,<br>num_movable_nodes)<br>  for cluster_id in range(cluster_factor):<br>    idx = np.where(node_clusters == cluster_id)[0]<br>    cluster_center_x = np.random.uniform(placedb.xl, placedb.xh)<br>    cluster_center_y = np.random.uniform(placedb.yl, placedb.yh)<br>    self.init_pos[idx] = np.random.normal(<br>      loc=cluster_center_x,scale=(placedb.xh - placedb.xl) / (15<br>* cluster_factor),size=len(idx))<br># Net-weight-informed noise addition<br># Iterative Refinement with Early Cooling<br>We omit these implementations and following parts to save area<br>(b) Discovered Initialization Example<br><!-- End of picture text -->

Fig. 2 Discovered algorithms example. 

framework that utilizes LLM to evolve optimization algorithms for global placement. Our framework focuses on three key optimization components: initialization, preconditioner, and optimizer. As shown in Fig. 1, the process begins by retrieving the original algorithm codes from the placement engine. These codes are then combined with carefully curated prompts for the LLM, which generates and refines new algorithm codes. The evolved algorithm codes are integrated back into the placement engine to produce the results. The evolution framework executes this process iteratively to generate and evolve optimization algorithms. The details of evolution framework includes algorithm candidates generation and evolution two processes. Specifically, we first generate large amounts of candidate algorithms offline via LLM, then we introduces an efficient LLM-based genetic flow to evolve chosen candidates. We leverage a large GPU cluster to accelerate whole evolution process to make it within a desired running time. Additionally, we introduce an algorithm-level design space exploration flow tailored for resource-constrained scenario. 

**Key Findings: LLM exhibit remarkable capabilities in evolving optimization algorithms, resulting in significant improvements in placement quality.** Fig. 2 provides an example for discovered initialization algorithm code snippet. Compared with DREAMPlace version which simply move x, y position to the center of layout with a simple noise addition for exploration purpose. The discovered algorithm leverages more net information and add more heuristics including adaptive density scaling, clustering, net-weight-informed noised addition and other heuristics to improve macro initialization. Fig. 3 compares our method with DREAMPlace-4.1 on the MMS benchmark adaptec1 design case. Our placement appears more compact, aesthetic and regularity. Quantitatively, our approach achieves over **10%** improvement in Half-Perimeter Wirelength (HPWL) compared to DREAMPlace-4.1. Note that placement is the core problem in EDA and even 1% HPWL improvement is not negligible. Our contributions are as follows: 

_•_ We propose an LLM-based algorithm evolution frame- 

work to design new algorithms effectively in placement problem. 

- Our results demonstrate significant improvement on several benchmarks under strict fair comparison, which shows the great potential of automatic algorithm design in EDA field. 

- We release all code, prompts, and discovered optimization algorithms, which can inspire researchers for further explorations. 

## II. RELATED WORKS 

_A. Heuristics and Customized Algorithms in Global Placement_ 

Heuristic and customized algorithms are widely used in global placement due to the problem’s NP-hard nature [27]. For instance, AutoDMP [40] introduces two parameters to set the initial cell location as a percentage of the width and height of the layout. [41] introduces a macro orientation refinement heuristic. RePlAce [11] introduces local and global density function with some heuristics implementations. DREAMPlace-4.0 [25] improves preconditioner by incorporating net-weighting information. DREAMPlace-4.1 [26] introduces a robust SA algorithm to solve legalization issues. RePlAce [11] proposes a dynamic step size adaptation method. ePlace [10] introduces Nesterov optimizer with tailored line search techniques, which incorporates carefully designed optimizer parameters. This work mainly focuses on mentioned three components while ignoring other heuristic parts. However, our framework can easily incorporate these heuristics and make it into a large evolution framework. 

## _B. Automatic Algorithm Design and Evolution_ 

Designing algorithms is labor-intensive and requires significant expertise. Recent works that leveraging LLM to design algorithms provide new perspective for this problem [38]. FunSearch [37] is the pioneer paper that leveraging LLM for algorithms generation and evolution targeting optimization problem such as bin packing. It defines an algorithm-level code prompt template including “evaluate”, “solve” and “heuristic” to prompt LLM to produce new heuristics and generate related code. The generated code is executed, and feedback is used to iteratively refine the heuristics and code through the LLM. Later several works follow this pattern and improve by introducing sophisticated prompt engineering such as evolve both heuristic and code [42], exploring multi-objective setting [43] and designing new cost functions [44]. However, current LLM for algorithm design approach does not touch complex NPhard industry challenges like placement [27], where LLM has to leverage placement knowledge prior to enhancing existing algorithms, such as initialization. 

## III. METHOD 

Our framework leverages LLM to evolve optimization algorithms for global placement task, specifically targeting three optimization components: initialization, preconditioner, and optimizer. The algorithm evolution process follows a 



<!-- Start of picture text -->
HPWL: 64.63  HPWL: 57.57<br>(a) DREAMPlace-4.1   (b) Ours<br><!-- End of picture text -->

Fig. 3 Comparison between DREAMPlace-4.1 and ours. 



<!-- Start of picture text -->
Initia algo Precond algo Optimizer algo<br>prompts & code<br>prompts & code LLM<br>prompts & code<br>(a) Step1: Algorithms Generation<br>Select Evolve Select Evolve Select Evolve<br>LLM LLM LLM<br>Leads to Leads to<br>(b) Step2: Algorithms Evolution<br><!-- End of picture text -->

Fig. 4 LLM-based Algorithm Generation and Evolution Pipeline. 

sequential pipeline where each component builds upon its predecessors. For example, the preconditioner is selected and evolved based on the evolved initialization algorithm. As shown in Fig. 4, our framework mainly contains two steps. In the first step, we employ LLM to generate diverse algorithm candidates for all three componenets offline (detailed in Section III-A). The generated candidates of each component are merged into placement engine and then evaluated in parallel on a GPU cluster. In the second step, rather than solely selecting top-performing algorithms, we implement a balanced selection strategy considering both performance and diversity as described in Section III-B. Finally, we apply genetic algorithms to evolve the selected candidates as outlined in Section III-C. 

Although the proposed LLM-based algorithm design demonstrates significant improvement, the running time is a new bottleneck in resource-constrained scenario. Therefore, we introduce a new algorithm-level design space (DSE) exploration to tackle the running-time problem as presented in Section III-D. 

## _A. Candidates Generation_ 

The candidate algorithm generation phase leverages LLM to produce a diverse set of feasible optimization algorithms. We design specialized prompts to guide LLM in generating the desired outputs. 

**Prompt Construction For Optimization Algorithms** . Fig. 5 demonstrates a simplified prompt template example. We use a 

markdown-style format to structure the prompt, which includes task description, context, algorithm code, related analysis, specific instructions and output format. While the basic template structure remains fixed, components like algorithm code and related analysis are dynamically updated. The template enforces clear instructions and output formats to ensure useful and structured responses from the LLM. 

**Chain-of-Thoughts Prompt Engineering** . We leverage Chain-of-Thoughts (CoT) [45] to enhance the algorithm generation process. The LLM first analyzes the current optimization algorithm, and this analysis is then incorporated into the new prompt template. This CoT approach provides richer context for algorithm generation. Additionally, the inherent variability in LLM’s analyses introduces beneficial randomness, leading to diverse candidate algorithms. 

**Leveraging Extra Placement Inputs** . Placement inputs such as logical netlist and physical cell library contain valuable patterns that can enhance optimization algorithms, yet effective extraction and utilization of such information remains a challenge. Despite efforts to utilize placement inputs, such as DREAMPlace-4.0 [25]improving preconditioner via incorporating different net-weighting, these expert-designed algorithms still cannot fully exploit latent patterns. We propose using LLM to dynamically select and leverage placement inputs. Fig. 6 shows partial placement inputs and a discovered algorithm with placement inputs example. The discovered algorithm generated by LLM makes use of some extra placement inputs (not used in default implementation) to improve algorithms. We collect placement inputs from the placement engine and integrate it into LLM prompts for automated feature selection and algorithm synthesis. Results indicate that LLMs can effectively synthesize sophisticated functions to extract valuable optimization insights from placement inputs. 

**Self-Referencing Prompt Engineering** . We also propose a self-referencing technique to improve candidate algorithm generation process. First, using previous outputs, we prompt the LLM to generate a high-level idea for a new optimization algorithm. Next, this high-level idea guides the LLM to produce corresponding code implementation. Finally, this implementation serves as a reference for generating the final placement-engine-format candidate algorithms. 

In general, the candidates are generated in four sequential steps: (1) LLM analyzes the given algorithm codes, (2) this analysis feeds into a new prompt template to generate highlevel idea, (3) the idea guide LLM to generate reference code implementation, and (4) the reference code helps generate final desired candidate algorithms. Each step uses slightly different prompt templates with customized instructions and output formats, with details omitted for brevity. 

## _B. Candidates Selection_ 

After generating _N_ candidate algorithms, we evaluate their HPWL performance in parallel using a GPU cluster. For the next evolution stage, we need to select top _−m_ high-performed algorithms. The greedy approach is to select the top _−m_ 



<!-- Start of picture text -->
# Task: Improve DREAMPlace Initialization Algorithm<br>## Context  - Problem: Analytical global placement in EDA…<br>## DREAMPlace Init Algo:<br>```python<br>[DREAMPlace Init Implementation Snippet Here] ```<br>## Analysis of Current DREAMPlace Init Algo<br>[COT Analysis Here]<br>## Instructions<br>[Detailed Instructions Here]<br>## Output Format<br>[Detailed Output Format Design Here]<br><!-- End of picture text -->

## **Algorithm 1** Evolution Flow 

- 1: **Input:** Sorted candidates **A** = _{_ **_a_ 1** _,_ **_a_ 2** _, · · · ,_ **_am_** _}_ and iterations _T_ ; 

- 2: **Output:** Best **_a_**<sup>**_∗_**</sup> ; 

- 3: **for** _t ←_ 1 to _T_ **do** 

- 4: Update UCB scores and choose the best **_a_**<sup>**_∗_**</sup> following Equation (4); 5: Evolve and Self-Reflect generated candidates **_am_ +1** via Equation (3); 6: **A** _←_ **A** _∪_ **_am_ +1** ; Sort candidates via HPWL; **A** _←_ **A** _\_ **_a_ 1** ; 7: **end for** 8: **return** Best **_a_**<sup>**_∗_**</sup> in candidate lists **A** ; 

Fig. 5 A Simplified Prompt Example. 

## _C. Candidates Evolution_ 



<!-- Start of picture text -->
Input Description<br>node s ize x cell width<br>node s ize y cell height<br>pin offset x pin offset x to node<br>pin offset y pin offset y to node<br>net w eights Weights for each net<br>total space a rea total placeable space area<br>total moveable n ode a rea total movable cell area<br>(a) Partial Placement Inputs<br>density_scaling = min(1.0, (placedb. total_space_area<br>- placedb.total_filler_node_area) /<br>placedb. total_movable_node_area )<br>center_x = (placedb.xl + placedb.xh) / 2<br>node_x_median = np.median(placedb.node_x[:num_movable_nodes])<br>self.init_pos[0:num_physical_nodes] = ((1 - density_scaling)<br>* node_x_median + density_scaling * center_x)<br>(b) Discovered Algorithm with Placement Inputs<br><!-- End of picture text -->

Fig. 6 Partial Placement Inputs. 

algorithm with the best HPWL scores. However, we notice that some high-performed algorithms often share similar highlevel ideas, which may cause redundant LLM generation and limit exploration on other candidates’ evolution. Therefore, we propose to select top _−m_ high-performed and diverse candidate algorithms _{_ **_a_ 1** _,_ **_a_ 2** _, · · · ,_ **_am_** _} ∈_ **A** by maximizing following objectives: 



where _f_ ( _·_ ) represents the objective function that returns negative normalized HPWL value, _dis_ ( _·_ ) function denotes the distance function which measure the negative cosine similarity between two algorithm embeddings. Equation (1) is an NPhard problem which can be reduced to the classical k-clique problem [46]. We provide a greedy solution to tackle this problem. We first prune the candidate selection space by selecting top _−k_ (k _>_ m) performing candidates. We then include the best candidate algorithm **_a_**<sup>**_∗_**</sup> into candidate lists because we observe that the best one is likely to “win” throughout the evolution process. Then we iteratively select algorithms **_ai_** into candidates lists by maximizing following objectives: 



After each selection step, we append the chosen one into candidate lists **A** . This process ends until we collect predefined _m_ candidates. 

After selecting candidate algorithms, we leverage LLM to evolve chosen algorithms through an iterative process. 

**Evolution Prompt Engineering** . The evolution prompt extends our candidate algorithm generation approach described in Section III-A, maintaining the use of CoT, extra placement inputs and self-reference techniques. We enhance this process by incorporating self-reflection prompt outputs into the evolution prompt to improve the given candidate algorithms. 

**Self-Reflection Prompt Engineering** . For each evolved algorithm, we integrate it into the placement engine and evaluate its HPWL performance. The self-reflection prompt mainly deals with three possible outcomes compared with the current best candidate: (1) execution failure of the evolved algorithm, (2) HPWL improvement, or (3) HPWL degradation. We combine the HPWL feedback into new prompt template and prompt the LLM to play a self-reflection [47] to refine the previously algorithm version. 

The whole evolution process iteratively executes evolution and self-reflection prompts to obtain evolved algorithms. We modify instructions and output format to get desired outputs. Denote LLM as _πθ_ , two evolution prompts as **_pe_ 1** and **_pe_ 2** , and reflect prompt as **_pr_** . **_pe_ 1** generates an initial evolution without reflection, while **_pe_ 2** incorporates reflection analysis. Given _m−_ th algorithm, the new evolved algorithm **_am_ +1** is given by: 



where **_a_** ˆ **_m_** is the extracted evolved algorithm generated from LLM via first evolution prompt. **_rm_** is the HPWL feedback of **_a_** ˆ **_m_** , **_r_** ˆ **_m_** is the self-reflection analysis. The final evolved algorithm **_am_ +1** is obtained from second evolution prompt with self-reflection analysis and previous algorithm versions. In practice, multiple evolution and self-reflection cycles can be executed in parallel for the selected candidate algorithm to improve evolution results. 

**Evolution Flow** . We select one candidate algorithm to evolve each iteration given _m_ candidate algorithms. To select the candidate algorithm effectively, we adopt the Upper Confidence Bound (UCB) algorithm [48], this involves choosing the best candidate algorithm **_a_**<sup>**_∗_**</sup> based on the evolution scores of each candidate algorithm at every step. We define _Q_ ( **_a_** ) as the normalized obtained HPWL scores for a selected candidate 

algorithm, _N_ ( **_a_** ) as the number of trials for this algorithm, and _t_ as the total number of trials. The algorithms selection is based on the following equations: 



The UCB algorithm, derived using Hoeffding’s inequality [49], offers a sublinear regret, providing an effective balance between exploring new candidates and exploitation. 

Algorithm 1 demonstrates our evolution pipeline. Given _m_ candidate algorithms, we select one candidate each time based on their UCB score as calculated by Equation (4). Then we evolve selected algorithms via evolution and selfreflection prompt through Equation (3). After evolution, we append the new evolved algorithms into candidate lists. We sort the candidate list with HPWL values and delete the worst one. This process iteratively evolve the candidate algorithms until it reaches the pre-defined iteration steps. 

## _D. Algorithm-level Design Space Exploration_ 

Despite the significant improvement discovered algorithms, the algorithm execution time is a potential bottleneck in resource constrained scenarios. Therefore, we propose an algorithm-level DSE framework to tackle this problem. Fig. 7 illustrates our Algorithm-level DSE framework, which combines offline pretraining and online search pipeline. For example, we pretrain on the ISPD2019 benchmark and leverage the surrogate model for the MMS benchmark. We employ an embedding model [28] to extract feature embeddings for candidate algorithms and a two-layer neural network to capture features from the placement inputs. These embeddings are concatenated, and a second two-layer neural network processes the combined features. The offline model is trained using HPWL results as supervision. 

Similar to conventional DSE settings [40], [50]–[53], we treat generated placement algorithms as design space and seek optimal solutions under time constraints (limited sampling). Our method employs Bayesian Optimization (BO) [54], [55] with two key components: a surrogate model for performance prediction with uncertainty estimates, and an acquisition function for efficient design space exploration. New design points are selected using the acquisition function and leveraged to update the surrogate model. We implement Gaussian process (GP) [56] as surrogate model, characterized by mean and variance functions. Each time given a new data point, GP updates accordingly. We use expected improvement (EI) [57] as acquisition function. Algorithm 2 demonstrates our Algorithmlevel DSE framework. We first randomly sample some design point from candidate lists and initialize GP and EI function. Then we iteratively update surrogate model GP based on sampled points via EI until reaching the pre-defined iterations. In the end, we obtain output set. 

In this work we only consider HPWL as objective. Therefore, we select the best evaluated algorithm in the end. However, our framework is compatible with multi-objective optimization problem. 

## **Algorithm 2** DSE Flow 

- 1: **Input:** All algorithm design space **A** and optimization steps _N_ ; 

- 2: **Output:** Pareto Set **P** , initially **P** _←∅_ ; 3: Randomly sample initial sets, initialize GP and EI function; 



<!-- Start of picture text -->
4: for n ← 1 to N do<br>5: Update surrogate model and EI based on sampled data;<br>6: a ∗ ← arg max a ∈ A  EI( a ) ;<br>7: Run Placement Engine with a ∗ to obtain feedback y ;<br>8: P ← P ∪ a ∗ ;<br>9: end for<br><!-- End of picture text -->

- 10: **return** Pareto Set from **P** ; 



<!-- Start of picture text -->
Offline Pretrain Bayesian Optimization<br>Placement Input Surrogate Model<br>�� Update<br>+ NN<br>��<br>embedding Supervise<br>Offline Evaluation Sampel Selection<br>Evaluation<br>Placement<br>Engine<br><!-- End of picture text -->

Fig. 7 Algorithm DSE framework. 

IV. EXPERIMENTAL RESULTS 

## _A. Implementation and Benchmarks_ 

We implement our framework on top of open-sourced DREAMPlace-4.1 [26]. To ensure reproducibility, we maintain all default hyper-parameters and settings as specified in [26] and fix random seeds to ensure stability of results. 

Our experiments utilize the GPT-4o API (version gpt-4o2024-08-06) and Embedding API (version text-embedding-3large). We leverage a distributed GPU cluster comprising 60 NVIDIA RTX 2080 Ti and 150 RTX 3090 GPUs for parallel execution. We generate at least 1000 feasible candidates for each optimization components. In evolution phase, the total trail numbers is 1000 for each case. 

We evaluate our algorithms on three benchmarks: MMS [58], ISPD2005 [59], and ISPD2019 [60]. MMS, derived from ISPD2005/ISPD2006, is a widely-used and competitive benchmark where all macros are movable and I/O object sizes are set to zero. We also use a modified version of the ISPD2005 benchmark, where macros and I/O objects are movable without altering their shapes, as introduced in [26]. ISPD2019, though originally a routing benchmark, can be adapted for placement problems, allowing us to demonstrate the generality of our framework. Additionally, we also observe over 5% HPWL improvement on the TILOS benchmark [61]. However, since some implementations in DREAMPlace-4.1 [26] have not yet open-sourced, we refrain from releasing full results to ensure reproducibility using publicly available code. 

## _B. Performance Analysis_ 

**Case-by-Case Results Analysis** . TABLE I and Tables II and III demonstrate case-by-case evolution results. In this setting, we evolve our algorithms via design case HPWL feedback, which is same to conventional data-driven RL methods 

TABLE I Results on MMS benchmarks based on case-by-case algorithms 

|Design<br>Case|Def<br>Status|ault DREA<br>HPWL|MPlace<br>Runtime|DREA<br>Status|MPlace w/ B<br>HPWL|B Method<br>Runtime|DREAM<br>Status|Place w/ B<br>HPWL|B Method<sup>_~~∗~~_</sup><br>Runtime|Status|HPWL|Ours<br>Runtime|TT|HPWL_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|adaptec1|✓|65.24|29.58|✓|64.63|26.09|✓|64.78|35.06|✓|**57.57**|28.75|0.15|**11.13%**|
|adaptec2|✓|76.07|174.88|✓|74.71|43.88|✓|73.89|50.43|✓|**71.64**|49.40|0.38|**3.05%**|
|adaptec3|✓|155.44|83.01|✓|155.58|79.11|✓|152.77|64.00|✓|**125.75**|76.85|0.44|**17.69%**|
|adaptec4|✓|142.72|102.79|✓|142.48|85.94|✓|141.63|50.93|✓|**119.86**|77.82|0.22|**15.37%**|
|adaptec5|✓|307.35|103.63|✓|306.84|92.71|✓|308.68|101.05|✓|**306.82**|101.12|0.65|**0.59%**|
|bigblue1|✓|85.16|39.29|✓|85.32|32.57|✓|85.25|32.14|✓|**78.64**|30.28|0.15|**7.75%**|
|bigblue2|✓|125.33|187.13|✓|125.33|164.33|✓|124.91|50.33|✓|**124.64**|47.80|0.18|**0.22%**|
|bigblue3|✓|270.87|181.51|✓|273.84|194.47|✓|269.98|225.35|✓|**257.70**|279.26|2.12|**4.55%**|
|bigblue4|✓|643.55|233.31|✓|642.88|282.51|✓|642.02|247.73|✓|**640.74**|246.91|1.46|**0.20%**|
|newblue1|✓|58.61|32.62|✓|59.33|34.45|✓|59.52|38.19|✓|**57.47**|42.22|0.21|**3.43%**|
|newblue2|✓|151.51|83.24|✓|152.87|80.42|✓|151.47|58.65|✓|**149.82**|76.12|0.43|**1.10%**|
|newblue3|_×_|448.59|118.01|✓|**270.08**|92.84|✓|295.03|139.80|✓|271.32|143.71|1.22|**8.04%**|
|newblue4|✓|223.40|54.21|✓|223.24|59.69|✓|230.04|60.81|✓|**218.39**|97.87|0.27|**5.06%**|
|newblue5|✓|**387.90**|132.79|✓|388.98|160.38|✓|403.11|191.51|✓|402.97|204.47|1.62|**0.03%**|
|newblue6|✓|406.33|148.31|✓|406.82|168.85|✓|407.03|115.91|✓|**405.68**|129.98|0.54|**0.33%**|
|newblue7|✓|879.37|281.74|✓|881.64|304.60|✓|883.68|232.04|✓|**866.64**|285.26|1.43|**1.93%**|
|Ratio||1.000|1.000||0.976|0.947||0.980|0.919||**0.931**|0.995||**5.05%**|



w/ BB Method<sup>_~~∗~~_</sup> indicates self-implementation version based on open-source code. TT indicates total runtime of whole evolution process, which is measured in hours. 

TABLE II Results on I/O-freed ISPD2005 benchmarks based on case-by-case algorithms 

|Design<br>Case|Defa<br>Status|ult DREA<br>HPWL|MPlace<br>Runtime|DREAM<br>Status|Place w/ B<br>HPWL|B Method<br>Runtime|DREAM<br>Status|Place w/ B<br>HPWL|B Method<sup>_~~∗~~_</sup><br>Runtime|Status|HPWL|Ours<br>Runtime|TT|HPWL_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|adaptec1|✓|67.91|122.99|✓|65.92|127.88|✓|72.71|31.34|✓|68.44|27.53|0.09|**5.87%**|
|adaptec2|✓|79.74|145.01|✓|77.65|143.08|✓|82.46|30.01|✓|80.99|32.55|0.11|**1.78%**|
|adaptec3|✓|153.51|162.94|✓|151.31|173.44|✓|133.61|78.37|✓|**127.60**|76.92|0.51|**4.50%**|
|adaptec4|✓|213.86|86.86|✓|141.45|85.94|✓|132.67|64.23|✓|**125.96**|62.73|0.30|**5.06%**|
|bigblue1|✓|83.60|137.89|✓|82.55|132.94|✓|82.56|35.60|✓|**80.90**|35.91|0.15|**2.01%**|
|bigblue2|_×_|273.28|151.88|✓|99.92|149.06|✓|98.75|138.47|✓|**91.98**|140.07|0.54|**6.86%**|
|bigblue3|✓|301.70|161.26|✓|296.79|197.04|✓|287.13|270.18|✓|**252.12**|237.08|2.14|**12.19%**|
|bigblue4|✓|658.75|285.61|✓|620.00|314.12|✓|612.45|295.67|✓|**587.77**|340.21|1.76|**4.03%**|
|Ratio||1.000|1.000||0.859|1.043||0.853|0.819||0.809|0.786||**5.29%**|



TABLE III Results on ISPD2019 based on case-by-case algorithms 

||DREA<br>HPWL|MPlace<br>Runtime|w/ BB <br>HPWL|Method<sup>_~~∗~~_</sup><br>Runtime|HPWL|Ours<br>Runtime|HPWL_↓_|
|---|---|---|---|---|---|---|---|
|Ratio|1.000|1.000|1.000|0.988|**0.906**|1.12|**8.30%**|
|ABL|E IV Re<br>DREA<br>HPWL|sults on <br>MPlace<br>Runtime|MMS b<br>w/ BB <br>HPWL|ased on g<br> Method<sup>_~~∗~~_</sup><br>Runtime|eneraliz<br>HPWL|ed algori<br>Ours<br>Runtime|thms<br>HPWL_↓_|
|Ratio|1.000|1.000|0.980|0.919|**0.974**|1.01|**0.509%**|



TABLE IV Results on MMS based on generalized algorithms 



<!-- Start of picture text -->
(a) adaptec1 (b) bigblue1<br><!-- End of picture text -->

Fig. 8 Rudy-RSMT Pareto frontiers comparison. 

TABLE V Results on ISPD2005 based on generalized algorithms 

||DRE|AMPlace|w/ BB|Method<sup>_~~∗~~_</sup>||Ours||
|---|---|---|---|---|---|---|---|
||HPWL|Runtime|HPWL|Runtime|HPWL|Runtime|HPWL_↓_|
|Ratio|1.000|1.000|0.853|0.819|**0.824**|0.83|**2.85%**|



TABLE VI Selected results on discovered initialization algorithms 

|Design|w/ BB|Method<sup>_~~∗~~_</sup>|Selec|ted Init Alg|orithm|
|---|---|---|---|---|---|
|Case|HPWL|Runtime|HPWL|Runtime|HPWL_↓_|
|adaptec1|64.78|35.06|61.45|37.95|5_._14%|
|adaptec3|152.77|64.00|129.86|71.71|14_._99%|
|adaptec4|141.63|50.93|123.85|56.48|12_._55%|
|bigblue1|85.25|32.14|78.98|35.65|7_._35%|



and recent algorithm design and evolution pipeline [37], [38], [62]–[67]. Default DREAMPlace indicates DREAMPlace-4.1 without Barzilai-Borwein method which we serve as a stable baseline. Note that This version’s performance is much better than the Default DREAMPlace performance in previous papers such as [26] because we use the latest open-source DREAMPlace version [26] with two-stage flow for mixed- 

size global placement and customized macro legalization. DREAMPlace w/ BB Method and DREAMPlace w/ BB Method<sup>_∗_</sup> indicates the results presented on original paper [26] and our self-implementation results. We provide two version’s results because case-by-case results may perform differently within different environments, sometimes even close to 1% difference. It can be shown that our self-implement obtains similar results compared with paper result [26]. Although some cases may have around 1% difference, such as case newblue3 on MMS benchmark and case adaptec3 and adaptec4 on ISPD2005 benchmark. Nevertheless, the overall HPWL performance ratio is stable. We observe the discovered algorithms demonstrate significant improvement on almost all cases while maintaining same-level running-time on top of DREAMPlace engine. Specifically, some cases such as adaptec1, adaptec3 on MMS and biglue3 on ISPD2005 all show over 10% HPWL improvement. Even greater gains are observed on the ISPD2019 benchmark, which, although primarily a routing benchmark, is rarely used in placement research. We high- 



<!-- Start of picture text -->
76 Runtime ( h ) AutoDMP Ours BB<br>5 HPWL HPWL SVM<br>4 Ratio 1.00 0.93 RT<br>3 XGB<br>21 Ours<br>0.1 0.5 1.0 0.9 0.95 1.0<br>Runtime Ratio Ours AutoDMP HPWL Ratio<br>(a) Versus AI Methods (b) Versus AutoDMP (c) DSE Comparison<br>WMMP EPOurs<br><!-- End of picture text -->

Fig. 9 DSE comparison and running-time results. 



<!-- Start of picture text -->
(a) adaptec1  (b) adaptec5  (c) ISPD2005<br>HPWL HPWL<br>Improvement<br><!-- End of picture text -->

Fig. 10 Discovered algorithm results observations. 

TABLE VII DSE results on IO-freed ISPD2005 benchmarks 

||Ours|(Exact)||Ours (DSE|)|
|---|---|---|---|---|---|
||HPWL|Runtime|HPWL|Runtime|Runtime_↓_|
|Ratio|1.000|1.000|1.037|0.165|**83.50%**|



light the generalization capability of our algorithm-evolution framework on this benchmark. There are two possible statuses: success (✓) and divergence ( _×_ ), where divergence indicates extremely low-quality solutions. We report the total runtime (TT) for each case, measured on GPU clusters using parallel execution. This runtime is acceptable for placement tasks and can be further reduced by adding more GPUs. Fig. 8 presents the results of combining our discovered algorithms with the AutoDMP parameter DSE method [40] on MMS benchmark. Our approach achieves better Rudy-RSMT Pareto frontiers than AutoDMP alone, demonstrating that our algorithms are compatible with parameter-tuning methods and can potentially improve other objectives such as RSMT. 

**Generalized Results Analysis** . TABLE IV and TABLE V show generalized results on MMS and ISPD2005 benchmarks, where a generalized algorithm is applied to all cases. Our generalized algorithm still achieves non-negligible improvements. Noted that we only test on our generated candidate algorithms without evolution parts, thus the algorithm candidates do not receive any HPWL feedback. However, although the general results are not comparable with the case-by-case evolution results, we still observe impressive generalized discovered algorithms as shown in Fig. 2. TABLE VI demonstrates the selected results on MMS benchmark based on this generalized discovered algorithm. It’s clearly that the discovered algorithm achieves significant improvement across different cases. Note that this discovered initialization algorithm is not general for all cases and it also produce divergence performance in other cases. However, due to the large improvement, we believe the discovered algorithms can provide new insights for researchers. 

**Runtime Analysis and DSE results** . We compare our total runtime with both data-driven RL methods [64], [66], [66], WM (WireMask), MP (MaskPlace) and EP (EfficientPlace), and the parameter-tuning method, AutoDMP [40] on ISPD2005 and MMS benchmarks. as shown in Fig. 9 (a) and (b), under the same case-by-case searching setting. Our method is faster than both approaches. In terms of HPWL performance, we find that RL methods still lag behind analytical approaches, based on our self-implementation with open-source code. Our approach also outperforms AutoDMP with a shorter runtime. We also provide an algorithm-level DSE method in 

resourced-constrained scenario. Fig. 9 (c) compares our method with SVM, RF (RandomForest) and XGB (XGBoost) on ISPD2005 benchmark. The x-axis shows the HPWL ratio, with BB method as the baseline. Under the same DSE setting with 100 design points selection, our method surpasses all others competitors within the same search time. TABLE VII shows the improvement of runtime compared with extract method, from which we use only one GPU to simulate resource-constrained scenario. The runtime of DSE method is largely reduced compared with extract method with less HPWL loss. 

## _C. Observations and Discussions_ 

**General Observations** . Due to space constraints, we omit some tables. Overall, we find that generating and evolving the initialization algorithm plays the most significant role in improving performance with minimal impact on DREAMPlace runtime. **The key insight is that macro position initialization is critical, often leading significant improvements.** Among the three algorithm components, initializations have the highest generation success rate, followed by optimizers, with preconditioners performing slightly worse. 

**Discovered Algorithm Observations** . Fig. 10 (a) and (b) illustrate two representative styles of discovered algorithms using the adaptec1 and adaptec5 cases from the MMS benchmark. The x-axis represents the algorithm index. In Fig. 10 (a), we observe a ”pyramid-like” pattern, where groups of algorithms with similar performance cluster together, and fewer algorithms achieve better HPWL as performance improves. In contrast, Fig. 10 (b) shows an ”emergence” phenomenon, where a single standout algorithm significantly outperforms the rest, appearing almost randomly. 

**Inference Scaling Phenomenon** . We also observe an interesting scaling phenomenon regarding the inference scaling law. Fig. 10 (c) shows the relationship between performance improvement and the number of generated algorithms on the ISPD2005 benchmark. We randomly select different sets of generated algorithms multiple times and average the improvements. Contrary to the conventional expectation of a linear relationship, the curve shows a clear ”logarithmic” trend. We will provide explorations in future work. 

## V. CONCLUSION 

In this work, we introduce a novel algorithm evolution framework for global placement utilizing large language models. The framework consists of two main components: an 

offline generation phase that creates diverse candidate algorithms, and an evolutionary process that combines selection strategies and genetic framework to improve chosen algorithms. We also provide an algorithm-level DSE solution targeting resource-constrained scenarios. The discovered algorithms achieve significant improvements on several benchmarks and demonstrate good generalization ability as well. We hope this work can provide new insights for this area. 

## REFERENCES 

- [1] J. A. Roy _et al._ , “Capo: robust and scalable open-source min-cut floorplacer,” in _ISPD_ , 2005. 

- [2] X. Yang, M. Sarrafzadeh _et al._ , “Dragon2000: Standard-cell placement tool for large industry circuits,” in _ICCAD_ . IEEE, 2000. 

- [3] J. A. Roy _et al._ , “Min-cut floorplacement,” _TCAD_ , vol. 25, no. 7, 2006. 

- [4] M.-C. Kim _et al._ , “Complx: A competitive primal-dual lagrange optimization for global placement,” in _DAC_ , 2012. 

- [5] ——, “Maple: Multilevel adaptive placement for mixed-size designs,” in _ISPD_ , 2012. 

- [6] T. Lin, C. Chu _et al._ , “Polar: Placement based on novel rough legalization and refinement,” in _ICCAD_ . IEEE, 2013. 

- [7] T. Chan _et al._ , “Multilevel generalized force-directed method for circuit placement,” in _ISPD_ , 2005. 

- [8] T.-C. Chen _et al._ , “NTUplace3: An analytical placer for large-scale mixed-size designs with preplaced blocks and density constraints,” vol. 27, no. 7, 2008. 

- [9] M.-K. Hsu _et al._ , “NTUplace4h: A novel routability-driven placement algorithm for hierarchical mixed-size circuit designs,” vol. 33, no. 12, 2014. 

- [10] J. Lu _et al._ , “ePlace: Electrostatics-based placement using fast fourier transform and Nesterov’s method,” vol. 20, no. 2, 2015. 

- [11] C.-K. Cheng _et al._ , “RePlace: Advancing solution quality and routability validation in global placement,” vol. 38, no. 9, 2018. 

- [12] Z. Zhu _et al._ , “Generalized augmented lagrangian and its applications to VLSI global placement,” 2018. 

- [13] W. C. Naylor _et al._ , “Non-linear optimization system and method for wire length and delay optimization for an automatic electric circuit placer,” Oct. 9 2001, uS Patent 6,301,693. 

- [14] C. Li _et al._ , “Recursive function smoothing of half-perimeter wirelength for analytical placement,” in _ISQED_ . IEEE, 2007. 

- [15] P. Spindler _et al._ , “Kraftwerk2—a fast force-directed quadratic placement approach using an accurate net model,” _TCAD_ , vol. 27, no. 8, 2008. 

- [16] M.-K. Hsu _et al._ , “Tsv-aware analytical placement for 3d ic designs,” in _DAC_ , 2011. 

- [17] ——, “Tsv-aware analytical placement for 3-d ic designs based on a novel weighted-average wirelength model,” _TCAD_ , vol. 32, no. 4, 2013. 

- [18] F.-K. Sun _et al._ , “Big: A bivariate gradient-based wirelength model for analytical circuit placement,” in _DAC_ , 2019. 

- [19] P. Liao _et al._ , “On a moreau envelope wirelength model for analytical global placement.” IEEE, 2023. 

- [20] J. Im and S. Kang, “Skyplace : A new mixed-size placement framework using modularlity-based clustering and sdp relaxation,” in _DAC_ . IEEE, 2024. 

- [21] N. Viswanathan _et al._ , “Fastplace 3.0: A fast multilevel quadratic placement algorithm with placement congestion control,” in _ASPDAC_ . IEEE, 2007. 

- [22] Y. Lin _et al._ , “Dreamplace: Deep learning toolkit-enabled gpu acceleration for modern vlsi placement,” in _DAC_ , 2019. 

- [23] ——, “Dreamplace 2.0: Open-source gpu-accelerated global and detailed placement for large-scale vlsi designs,” in _CSTIC_ . IEEE, 2020. 

- [24] J. Gu _et al._ , “DREAMPlace 3.0: Multi-electrostatics based robust VLSI placement with region constraints,” 2020. 

- [25] P. Liao _et al._ , “DREAMPlace 4.0: Timing-driven global placement with momentum-based net weighting.” IEEE, 2022. 

- [26] Y. Chen _et al._ , “Stronger mixed-size placement backbone considering second-order information.” IEEE, 2023. 

- [27] M. R. Garey _et al._ , “Some simplified np-complete problems,” in _STOC_ , 1974. 

- [28] J. Achiam _et al._ , “Gpt-4 technical report,” _arXiv_ , 2023. 

- [29] M. Liu _et al._ , “Chipnemo: Domain-adapted llms for chip design,” _arXiv_ , 2023. 

- [30] ——, “Verilogeval: Evaluating large language models for verilog code generation,” in _ICCAD_ . IEEE, 2023. 

- [31] S. Thakur _et al._ , “Benchmarking large language models for automated verilog rtl code generation,” in _DATE_ . IEEE, 2023. 

- [32] Y. Fu _et al._ , “Gpt4aigchip: Towards next-generation ai accelerator design automation via large language models,” in _ICCAD_ . IEEE, 2023. 

- [33] S. Liu _et al._ , “Rtlcoder: Outperforming gpt-3.5 in design rtl generation with our open-source dataset and lightweight solution,” in _LAD_ . IEEE, 2024. 

- [34] D. Saha _et al._ , “Llm for soc security: A paradigm shift,” _IEEE Access_ , 2024. 

- [35] K. Chang _et al._ , “Data is all you need: Finetuning llms for chip design via an automated design-data augmentation framework,” in _DAC_ , 2024. 

- [36] Y. Lai _et al._ , “Analogcoder: Analog circuit design via training-free code generation,” _arXiv_ , 2024. 

- [37] B. Romera-Paredes _et al._ , “Mathematical discoveries from program search with large language models,” _Nature_ , vol. 625, no. 7995, 2024. 

- [38] F. Liu _et al._ , “A systematic survey on large language models for algorithm design,” _arXiv_ , 2024. 

- [39] S. S. Seiden, “On the online bin packing problem,” _JACM_ , 2002. 

- [40] A. Agnesina _et al._ , “Autodmp: Automated dreamplace-based macro placement,” in _ISPD_ , 2023. 

- [41] C.-w. Sham _et al._ , “Optimal cell flipping in placement and floorplanning,” in _DAC_ . IEEE, 2006. 

- [42] F. Liu _et al._ , “Evolution of heuristics: Towards efficient automatic algorithm design using large language model,” in _ICML_ , 2024. 

- [43] S. Yao _et al._ , “Multi-objective evolution of heuristic using large language model,” _arXiv_ , 2024. 

- [44] Y. Yao _et al._ , “Evolve cost-aware acquisition functions using large language models,” in _PPSN_ . Springer, 2024. 

- [45] J. Wei _et al._ , “Chain-of-thought prompting elicits reasoning in large language models,” _NeurIPS_ , vol. 35, 2022. 

- [46] C. Tsourakakis, “The k-clique densest subgraph problem,” in _WWW_ , 2015. 

- [47] J. Huang _et al._ , “Large language models can self-improve,” _arXiv_ , 2022. 

- [48] A. Slivkins _et al._ , “Introduction to multi-armed bandits,” _Foundations and Trends® in Machine Learning_ , vol. 12, no. 1-2, 2019. 

- [49] P. Auer, “Using confidence bounds for exploitation-exploration tradeoffs,” _Journal of Machine Learning Research_ , vol. 3, no. Nov, 2002. 

- [50] J. Zhao _et al._ , “Comba: A comprehensive model-based analysis framework for high level synthesis of real applications,” in _ICCAD_ . IEEE, 2017. 

- [51] B. C. Schafer and Z. Wang, “High-level synthesis design space exploration: Past, present, and future,” _TCAD_ , vol. 39, no. 10, 2019. 

- [52] C. Bai _et al._ , “Boom-explorer: Risc-v boom microarchitecture design space exploration framework,” in _ICCAD_ . IEEE, 2021. 

- [53] A. Sohrabizadeh and Others, “Autodse: Enabling software programmers to design efficient fpga accelerators,” _TODAES_ , vol. 27, no. 4, 2022. 

- [54] J. Snoek _et al._ , “Practical bayesian optimization of machine learning algorithms,” _NeurIPS_ , 2012. 

- [55] W. Lyu _et al._ , “Batch bayesian optimization via multi-objective acquisition ensemble for automated analog circuit design,” in _ICML_ . PMLR, 2018. 

- [56] C. Williams _et al._ , “Gaussian processes for regression,” _NeurIPS_ , vol. 8, 1995. 

- [57] J. Moˇckus, “On bayesian methods for seeking the extremum,” in _IFIP_ . Springer, 1975. 

- [58] J. Z. Yan _et al._ , “Handling complexities in modern large-scale mixed-size placement,” in _DAC_ , 2009. 

- [59] G.-J. Nam _et al._ , “The ispd2005 placement contest and benchmark suite,” in _ISPD_ , 2005. 

- [60] S. Dolgov _et al._ , “2019 cad contest: Lef/def based global routing,” in _ICCAD_ . IEEE, 2019. 

- [61] C.-K. Cheng _et al._ , “Assessment of reinforcement learning for macro placement,” 2023. 

- [62] A. Mirhoseini _et al._ , “A graph placement methodology for fast chip design,” _Nature_ , vol. 594, no. 7862, 2021. 

- [63] R. Cheng and J. Yan, “On joint learning for solving placement and routing in chip design,” _NeurIPS_ , vol. 34, 2021. 

- [64] Y. Lai _et al._ , “Maskplace: Fast chip placement via reinforced visual representation learning,” _NeurIPS_ , vol. 35, 2022. 

- [65] ——, “Chipformer: Transferable chip placement via offline decision transformer,” in _ICML_ . PMLR, 2023. 

- [66] Y. Shi _et al._ , “Macro placement by wire-mask-guided black-box optimization,” _NeurIPS_ , vol. 36, 2024. 

- [67] Z. Geng _et al._ , “Reinforcement learning within tree search for fast macro placement,” in _ICML_ , 2024. 

