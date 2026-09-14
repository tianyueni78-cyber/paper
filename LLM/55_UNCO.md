BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

1 

# Bridging Large Language Models and Optimization: A Unified Framework for Text-attributed Combinatorial Optimization 

Xia Jiang, Yaoxin Wu, Yuan Wang, and Yingqian Zhang 

**_Abstract_ —To advance capabilities of large language models (LLMs) in solving combinatorial optimization problems (COPs), this paper presents the Language-based Neural COP Solver (LNCS), a novel framework that is unified for the end-to-end resolution of diverse text-attributed COPs. LNCS leverages LLMs to encode problem instances into a unified semantic space, and integrates their embeddings with a Transformer-based solution generator to produce high-quality solutions. By training the solution generator with conflict-free multi-task reinforcement learning, LNCS effectively enhances LLM performance in tackling COPs of varying types and sizes, achieving state-of-the-art results across diverse problems. Extensive experiments validate the effectiveness and generalizability of the LNCS, highlighting its potential as a unified and practical framework for real-world COP applications.** 

**_Index Terms_ —Combinatorial optimization, Neural network, Large language model, Reinforcement learning.** 

## I. INTRODUCTION 

Large language models (LLMs) have revolutionized artificial intelligence, demonstrating remarkable capabilities across various domains such as language understanding [1], [2], code generation [3], [4] and mathematical reasoning [5], [6]. Recently, there has been a growing trend in investigating the application of LLMs in automatically solving combinatorial optimization problems (COPs). 

COPs represent a fundamental class of mathematical problems that focuses on finding optimal solutions from finite sets of objects. Typical examples of COPs include the traveling salesman problem (TSP), the vehicle routing problem (VRP), the knapsack problem (KP), etc., which are challenging to solve due to the NP-hardness. COPs have been approached using exact methods or (meta-)heuristics in operations research [7], while recent neural combinatorial optimization (NCO) methods have emerged as promising alternatives [8]. However, these methods require domain expertise and specialized designs for each specific COP, hindering their applications to diverse COPs. In contrast, recent research has turned to LLMs to tackle COPs through natural language interactions (i.e., prompting), with the aim of further enhancing the automation of the problem solving process [9], [10], [11]. 

Xia Jiang, Yaoxin Wu, and Yingqian Zhang are with the Department of Industrial Engineering and Innovation Sciences, Eindhoven University of Technology, 5600 MB Eindhoven, The Netherlands (email: summer142857.jiang@gmail.com; wyxacc@hotmail.com; yqzhang@tue.nl). Yuan Wang is with Shenzhen Research Institute of Big Data, Shenzhen, China (email: wangyuan@cuhk.edu.cn) 

However, achieving high-quality solutions solely by prompting LLMs remains challenging, even for middle-sized COPs (e.g., those with above 50 nodes) [9]. Studies have indicated that LLMs often struggle with processing problems involving lengthy contexts, as they tend to lose coherence and accuracy in extended language descriptions [12]. Furthermore, LLMs often struggle to effectively comprehend and represent the intricate relationships between problem elements, such as graph structures in COPs. The inherently verbose and potentially ambiguous nature of COP descriptions in natural language raises considerable concerns about the ability of LLMs to independently generate satisfactory solutions. 

Despite these challenges, LLMs have gained considerable advantages in developing sophisticated linguistic knowledge and semantic representation, through their pretraining [13]. Their ability to represent natural language opens opportunities for integration with additional neural networks to address downstream text-based tasks, such as node classification and link prediction on text-attributed graphs [14], [15]. Specifically, LLMs can also encode descriptions of COPs, aligning them in a unified semantic space. A much lighter-weight network (compared to LLMs) can then leverage the aligned embeddings to generate solutions across problems. 

This paper presents the **L** anguage-based **N** eural **C** OP **S** olver (LNCS), a novel framework that integrates LLMs with a Transformer-based neural network to process text-attributed COPs and generate solutions. Concretely, it utilizes LLMs to encode text-attributed instances (TAIs) of different COPs into a shared semantic space. The semantic embeddings of TAIs are further processed by a Transformer network, which learns solution construction rules to generate solutions. By training the Transformer with reinforcement learning (RL) while freezing LLM parameters, LNCS borrows the LLM’s capability for generic representation of problem descriptions, and gains satisfactory performance to solve various COPs in a unified manner. 

Our main contributions are threefold: 1) we propose the LNCS to synthesize LLMs’ semantic representations with a Transformer network for solution generation, bridging LLMs and text-attributed COPs for end-to-end problem resolution; 2) we incorporate a conflict-free multi-task RL algorithm to facilitate the training for diverse COPs with varying scales of gradients through a unified model; 3) we evaluate LNCS on different text-attributed COPs, showcasing that LNCS outperforms typical prompting and optimization approaches. Moreover, we extensively validate the effectiveness and gen- 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

2 

eralizability of LNCS, which can be favorably fine-tuned for COPs of varying sizes and types. 

To the best of our knowledge, this work represents the first successful application of LLMs to build a unified (Transformer) model for solving general text-attributed COPs. It creates a vital connection between the linguistic capabilities of LLMs and their enhanced performance in COPs tasks. 

[37] and evolutionary algorithms [38], by employing neural networks to iteratively improve an initial solution. 

In contrast to NCO methods, the LNCS framework aims to address general text-attributed COPs described by natural language. It provides a single model for diverse COPs by leveraging LLMs’ unified semantic representations of texts. 

## III. PRELIMINARIES 

## II. RELATED WORK 

## _A. LLM for Optimization_ 

Research on the use of LLMs for optimization tasks has progressed along two main paradigms: approaches that use _LLMs as programmers_ to generate solution functions and those that employ _LLMs as optimizers_ to directly produce solutions. **LLMs as Programmers.** Recent advances showcase that LLMs are capable of writing programs to implement heuristic algorithms to solve COPs [16], [11]. Starting from an initial code template, LLMs can iteratively refine heuristics through an evolutionary process [17], [18]. However, the development of effective algorithms through this evolutionary process often necessitates substantial domain knowledge and token consumption for each specific COP. A more pragmatic approach enables LLMs to interface with established optimization solvers, such as Gurobi and OR-tools [19], [20]. These methods generally focus on formulating a COP instance using mathematical programming models [21], but they struggle to guarantee the correctness of the generated formulations, and thus are not applicable to real world scenarios. 

**LLMs as Optimizers.** LLMs can also function as black-box optimizers, which directly generate solutions [22] or iteratively refine an initial solution [9], [23]. Prompting techniques are pivotal in these approaches to solving COPs from language descriptions. However, current methods still present a substantial research gap in achieving high-quality solutions [11]. Research by [24] suggests that LLMs tend to memorize limited patterns in training data rather than develop generalizable reasoning skills, which impedes their effectiveness as direct optimizers. 

In this paper, the LNCS brings a novel paradigm to integrate LLMs with a Transformer network. Compared to the above paradigms, the LNCS enables LLMs to optimize diverse COPs through a single solution generator (i.e., the Transformer network), and enhance their capacity to solve COPs. 

## _B. Neural Combinatorial Optimization_ 

The constructive NCO methods aim to learn policies to construct solutions in an autoregressive way. The early attempts are based on pointer networks [25], [26], a class of recurrent neural networks (RNNs) that process the input and generate the solution in a sequence-to-sequence fashion. Inspired by the Transformer [27], the attention model (AM) is presented to solve VRPs, respectively, showing the advantage over conventional heuristics. Afterward, a series of strategies are proposed to enhance Transformer-based NCO models by leveraging the symmetricity of COPs [28], [29], [30] and efficient active search [31], [32], [33]. In addition, the improvement NCO methods enhance stochastic search algorithms, such as local search [34], [35], neighborhood search [36], 

## _A. Combinatorial Optimization Problems_ 

Solving a COP involves searching for an object within a finite (or countably infinite) discrete set, where the object can be an integer, a subset, or a permutation [7]. Most COPs could be represented on graphs in which objects are denoted by nodes and edges. More formally, a COP _P_ is formulated as follows: 



where **_x_** = _{x_ 1 _, ..., xn}_ is a set of discrete decision variables, defined by _{xi ∈ Di}_<sup>_n_</sup> _i_ =1<sup>;</sup><sup>_f_(</sup><sup>**_x_**</sup><sup>_, P_)denotesanobjective</sup> function to be minimized and _{cj_ ( **_x_** _, P_ ) _}_<sup>_J_</sup> _j_ =1<sup>denotesaset</sup> of problem-specific constraints for variables **_x_** . The set of all feasible solutions is denoted as: 



where we omit the subscript of _c_ ( **_x_** _, P_ ) for clarity. The optimal solution of a COP instance **_s_**<sup>_∗_</sup> _∈ S_ should satisfy _f_ ( **_s_**<sup>_∗_</sup> _, P_ ) _≤ f_ ( **_s_** _, P_ ) _, ∀_ **_s_** _∈ S_ . Typical COPs such as TSP, VRP, KP are well-known NP-hard problems due to their inherent computational complexity, making them difficult to solve optimally. The COPs involved in the paper are further detailed in Appendix A. 

## _B. Transformer for COPs_ 

Transformer can be used to construct solutions to COPs [39], [28], [40]. Concretely, the numerical features of a COP instance _G_<sup>_P_</sup> are encoded by an embedding layer, and then updated by an encoder. The global representation learned by the encoder, along with the context representation (e.g., the embedding of the partial tour in construction), is taken as input to the decoder. Next, the decoder is used to iteratively output the probabilities of candidate nodes. The decoding procedure ends when all nodes are selected one by one, according to the probabilities at each iteration. The probabilistic chain rule for constructing a solution _π_ is _p_ **_θ_** ( _π|G_<sup>_P_</sup> ) = � _ttf_ =1<sup>_pθ_(</sup><sup>_πt|GP , π<t_),where</sup><sup>_tf_referstothenumberoftotal</sup> iterations; _πt_ and _π<t_ denote the selected node and the current partial solution at the iteration _t_ . The Transformer is often trained by REINFORCE algorithm [41] with the gradients computed by: 



where E _p_ ( **_θ_** )( _π|GP_ ) _f_ ( _π_ ) is the expected cost of solutions and _b_ ( _·_ ) is a baseline for reducing estimation variance. We refer interested readers to Appendix B for more details on Transformer for COPs. 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

3 



Fig. 1: The illustration of the proposed framework. [ _Blue part_ ]: The LLM is frozen and takes as input the TAI for different COPs, producing task embedding and initial node embedding. [ _Orange part_ ]: The encoder of the trainable solution generator processes the embedding through the attention blocks and produces instance embeddings, which is further used to construct solutions by a decoder. 

## IV. METHODOLOGY 

## _A. TAIs of COPs_ 

Despite that the formations of various COPs (as displayed in Eq. (1)) would be different, they can generally be described in natural language. As shown in Figure 1, we propose to represent COP instances as text-attributed instances (TAIs) through task and instance descriptions. The task description specifies the formation of a COP, including decision variables, general constraints, and the objective function, while the instance description specifies the details of nodes or edges on the COP graph. 

Formally, the TAI of a COP _P_ is denoted as _I_ ( _G_<sup>_P_</sup> ) = _{κ_<sup>_P_</sup> _, v_<sup>_P_</sup> _}_ , which encapsulates both the task description _κ_<sup>_P_</sup> and the instance description _v_<sup>_P_</sup> , thus enabling the recognition of different COP instances. The task description _κ_<sup>_P_</sup> aims to prompt the LLM with the definition and background of the target COP, while the instance description _v_<sup>_P_</sup> offers details in an instance, e.g., features on nodes. 

Taking the instance description in Figure 1 as the example, the sentences _vi_<sup>_P_</sup> _∈ v_<sup>_P_</sup> _, i ∈{_ 1 _, . . . , n}_ delineates the numerical attributes on the nodes of an instance, indicating the basic features such as the node coordinates in TSP or the weight-profit pairs in KP. Additionally, we also incorporate heuristic information. By doing so, we aim to prompt the LLM to better understand each instance from the perspective of general and conventional heuristics. For example, according to greedy heuristics, we delineate the top- _k_ ( _k_ = 3) nearest nodes of each node in the instance description of TSP, and the value-to-weight ratios with their ranks in KP instances. The inclusion of heuristic information enhances the LLMs’ ability to comprehend the instances, which will be shown in the ablation study. 

## _B. Language-based Neural COP Solver_ 

Since LLMs cannot effectively solve COPs relying solely on their internal knowledge, the proposed LNCS integrates a Transformer with an LLM, as illustrated in Figure 1. The 

task and instance descriptions are individually taken as input by the LLM, with their embeddings obtained from the last layer of the LLM. Specifically, both the instance and the task description are processed by the LLM, which is expressed by _x_<sup>_P_</sup> _i_ = LLM( _vi_<sup>_P_)and</sup><sup>_kP_=LLM(</sup><sup>_κP_).Theembeddings</sup> _{x_<sup>_P_</sup> _i_<sup>_}n_</sup> _i_ =1<sup>containtheinformationpertainingtotheinstance,</sup> while task embedding _k_<sup>_P_</sup> reflects the domain-specific information of the COP _P_ . 

Inspired by AM [39], we develop a Transformer network in LNCS, which is shown in Figure 1, connecting to an LLM and serving as a solution generator for various text-attributed COPs. As the embeddings of different COPs are aligned within the same semantic space by the LLM, a single Transformer can easily process these embeddings without requiring any additional problem-specific modules. We elaborate the components of the solution generator as follows: 

**Connector.** Given the embeddings of TAIs, we use a linear projection layer to connect the LLM and the following attention blocks. As the embeddings produced by an LLM are typically high-dimensional, the connector with parameters **W**<sup>_e_</sup> _∈_ R<sup>_do×dh_</sup> and **b**<sup>_e_</sup> _∈_ R<sup>_dh_</sup> is used for dimensionality reduction. As such, the instance embeddings _{x_<sup>_P_</sup> _i_<sup>_}n_</sup> _i_ =1<sup>are</sup> concatenated into **x**<sup>_P_</sup> _∈_ R<sup>_n×do_</sup> and then linearly transformed by **h**<sup>(0)</sup> = **W**<sup>_e_</sup> **x**<sup>_P_</sup> + **b**<sup>_e_</sup> with **h**<sup>(0)</sup> _∈_ R<sup>_n×dh_</sup> . 

**Encoder. h**<sup>(0)</sup> is processed by successive attention blocks, each of which consists of a multi-head attention ( **MHA** ) layer [27], a node-wise FeedForward ( **FF** ) layer, a skipconnection layer [42] and a batch normalization ( **BN** ) layer [43], that is, 





where _l ∈{_ 1 _, . . . , N }_ represents the index of the attention block. The details of **MHA** , **FF** , and **BN** are elaborated in Appendix C. After _N_ attention blocks, the instance embeddings of a TAI are advanced to **h**<sup>(</sup><sup>_N_)</sup> _∈_ R<sup>_n×dh_</sup> . 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

4 

**Decoder.** The decoding is sequentially unfolded. In each step _t ∈{_ 1 _, ..., n}_ , a node is chosen to be appended to the partial solution until a feasible solution is constructed. The decoder should construct the solution for diverse COPs by 1) discriminating different COPs and 2) using a unified decoding process for various COPs. To this end, we need to define the decoding context to incorporate problem-specific information, which is then used to guide specific decoding policies for different COPs. 

One feasible way for the decoder to distinguish between different COPs is to provide it with the task description and problem-specific constraints. Given that some COPs entail dynamic constraints, such as the constraints defined by the varying vehicle load and knapsack capacity in the Capacitated VRP (CVRP) and KP, we first incorporate these dynamic attributes into the decoding context. We use a variable _c_<sup>_P_</sup> _t_ to monitor these dynamic attributes, indicating the remaining vehicle load _Ct_<sup>_v_orknapsackcapacity</sup><sup>_C_</sup> _t_<sup>_b_ateachdecoding</sup> step _t_ , such that: 



Note that we only take CVRP and KP as examples. One can easily extend it to encompass dynamic attributes of constraints in other COPs. 

Besides the dynamic attribute _c_<sup>_P_</sup> _t_<sup>andtaskembedding</sup><sup>_kP_,</sup> which involve task-specific information in the decoding context, the probability of selecting a node _πt_ at step _t_ should also be associated with the state of the current partial solution. Therefore, the final decoding context constitutes **c**<sup>_P_</sup> _t_<sup>,</sup><sup>_kP_,</sup><sup>_π<t_.</sup> Following [39], we use the embeddings of the first and last selected node, i.e., **h**<sup>(</sup> 1<sup>_N_)</sup> and **h**<sup>(</sup> _t_<sup>_N_)</sup> , to represent the partial solution _π<t_ . The context is formulated as: 



where [ _·, ·, ·, ·_ ] indicates a horizontal concatenation operation. Specially, we do not use the context at the first decoding step. Instead, we specify all nodes to start constructing _n_ solutions in parallel, which facilitate the exploration of solution space for performance enhancement [28]. 

Subsequently, the context **h**<sup>_t_</sup> ( _c_ )<sup>istakenasthequeryin</sup> an **MHA** layer, while the key and value are derived from **h**<sup>(</sup><sup>_N_)</sup> by linear transformations. The compatibility between the decoding context **h**<sup>_t_</sup> ( _c_ )<sup>andthekeyiscalculatedby:</sup> 



The logit for selecting node _i_ is calculated by: 



where _dA_ is the hidden dimension of the **MHA** layer; _C_ = 10 is the parameter for logit clipping; **h** _j_ is the embedding of node _i_ in **h**<sup>(</sup><sup>_N_)</sup> . Provided that the constraints cannot be satisfied by selecting node _i_ (e.g., the constraint is violated 



<!-- Start of picture text -->
0.2<br>0.0<br>0.2<br>Negative similarity<br>Positive similarity<br>0.4<br>0 500 1000 1500 2000<br>Iteration<br>Cosine Similarity<br><!-- End of picture text -->

Fig. 2: The cosine similarities between gradients of loss functions for 5 COPs (with _n_ = 50). The gradients are calculated during training the LNCS by 2000 batches, following the vanilla averaged REINFORCE. 

by _i_ = _πt_<sup>_′_</sup> _, ∀t′ < t_ for TSP), the corresponding logit _ui_ is set to _−∞_ . Finally, the decoder selects a node _πt_ at step _t_ by sampling from according to _p_ ( _πt_ ) = Softmax( _{ui}_<sup>_n_</sup> _i_ =1<sup>).</sup> The decoder iteratively selects nodes to construct a feasible solution until no more candidate nodes remain. 

## _C. Training Scheme_ 

We resort to RL to train the solution generator in the LNCS, while freezing the parameters of the LLM. Treating each COP as a task, one approach to training with multiple tasks is to average their RL losses for gradient backpropagation [44]. However, this simple averaging scheme for clearly different types of COPs presents a challenge in optimizing neural networks [45]. It may yield undesirable outcome for two reasons: Firstly, the objectives of different COPs may exhibit varying scales, making the larger gradients dominate the update of the model. Secondly, the updated directions of parameters may conflict under different objectives, potentially leading to performance degradation for specific COPs. These limitations will compromise the ability of LLMs to unify semantic representation for different COPs. To showcase the issue, we calculate the cosine similarities to determine if the gradients between tasks are contradictory, with the results plotted in Figure 2. As observed, the update directions of gradients for different COPs indeed have considerable conflicts, i.e., negative cosine similarity, which potentially harms the training of the model. 

To overcome the issue, we use a simple yet effective multi-task RL algorithm, named conflict gradients erasing reinforcement learning (CGERL), to train the LNCS. Inspired by [46], we project the conflicting gradients onto the normal plane of others, thereby enabling the model to share common knowledge from different COPs in a favorable conflict-free manner. Formally, suppose that we have a set of tasks _{Pi}_<sup>_N_</sup> _i_ =1 denoting _N_ different COPs. Let **g** _i_ and **g** _j_ denote the gradients of tasks _Pi ∈{Pi}_<sup>_N_</sup> _i_ =1<sup>and</sup><sup>_Pj∈{Pi}_</sup> _i_<sup>_N_</sup> =1<sup>,respectively.Each</sup> of the gradients can be estimated by Eq. (3), following the typical REINFORCE algorithm [41]. Afterward, we compute _δ_ = **g** _i ·_ **g** _j_ to determine whether the two gradients are conflicting ( _δ <_ 0) or not ( _δ ≥_ 0). As such, the gradient 

5 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

for task _Pi_ can be adapted by: 



The conflict elimination process is conducted for each training batch, consisting of multiple tasks. For each target task _Pi ∈ {Pi}_<sup>_N_</sup> _i_ =1<sup>,wesampleothertasks</sup><sup>_Pj_,</sup><sup>_∀j̸_=</sup><sup>_i_inrandomorder</sup> and progressively apply Eq. (10). The process repeats until the gradients of all tasks are adapted. Finally, the adapted gradients are aggregated as **g** =<sup>�</sup><sup>_N_</sup> _i_<sup>**g**ˆ</sup><sup>_i_,whichisusedtoupdatethe</sup> solution generator. The overall training procedure is provided in Appendix D. 

||Method<br>|_n_= 20<br>|_n_= 50<br>|_n_= 100<br>|
|---|---|---|---|---|
||AEL<br>|7.78%<br>|10.50%<br>|12.35%<br>|
||ReEvo<br>|7.77%<br>|10.23%<br>|11.87%|
|_SP_|SGE<br>|11.32%|45.28%|-|
|_T_|LMEA<sup>_∗_</sup><br>|3.94%|-|-|
||ORPO<sup>_∗_</sup><br>|4.40%<br>|133.0%<br>|-<br>|
||LNCS (ours)<br>|**0.39%**<br>|**1.64%**<br>|**4.38%**<br>|
|_P_|ReEvo<br>|5.19%<br>|14.27%<br>|19.59%|
|_VR_|SGE<br>|76.46%<br>|144.21%<br>|-<br>|
|_C_|LNCS (ours)<br>|**2.51%**<br>|**3.62%**<br>|**5.59%**<br>|
||ReEvo|0.14%|4.31%|9.40%|
|_KP_|SGE<br>|42.62%<br>|39.08%<br>|-<br>|
||LNCS (ours)|**0.10%**|**0.06%**|**0.03%**|



TABLE I: The optimality gaps of LLM-based approaches on TSP. *: Results are drawn from the original literature and based on gpt-3.5turbo. -: Excessively long computation time leads to the unavailability of results. 

## V. EXPERIMENTS 

We mainly use Llama2-7b [47] as the LLM for the evaluation of the method. We also provide an ablation study to test the performance of other language models. More details of the experiment settings, including model configuration and training process are provided in Appendix E. 

## _A. Benchmarks_ 

The proposed LNCS is evaluated on five representative COPs, including TSP, CVRP, KP, minimum vertex cover problem (MVCP), and single-machine total weighted tardiness problem (SMTWTP). Meanwhile, we fine-tune the trained LNCS on two new tasks, including the VRP with backhauls (VRPB) and the maximum independent set problem (MISP). The instance generation for the COPs and the examples of their TAIs are provided in Appendix F. Note that many other COPs can also be incorporated besides the above problems. 

## _B. Baselines_ 

**LLM-based Optimization:** We first compare our NLCS approach with other LLM-based methods, encompassing both _LLMs as programmers_ and _LLMs as optimizers_ , as outlined below: 

We use Algorithm Evolution Using LLMs (AEL) [48], Reflective Evolution (ReEvo) [18], and Self-Guiding Exploration (SGE) [11] as baselines for _LLMs as programmers_ , which leverage embedded knowledge to generate heuristics to solve COP. AEL and ReEvo are utilized to evolve constructive heuristics for solving the TSP, while ReEvo is also used to improve the ant colony optimization (ACO) for solving CVRP and KP. In addition, we include LLM-driven Evolutionary Algorithms (LMEA) [23] and Optimization by PROmpting (OPRO) [9] as baselines for _LLMs as optimizers_ , which attempt to directly produce solutions from textual problem descriptions. 

**Traditional Solvers:** We employ OR-Tools, which integrates various heuristic approaches, to solve TSP, CVRP, and KP. Additionally, we also use the Gurobi solver to obtain optimal solutions for the COPs and accordingly calculate the optimality gaps to evaluate other methods. 

The LNCS is also compared with conventional heuristics, such as the nearest neighbor and the farthest insertion for TSP, the sweep heuristic and parallel saving algorithm for 

CVRP [49], the greedy policy for KP, the MVCApprox method (i.e., greedily reduces costs over edges and iteratively builds a cover) [50] and the randomized edge-based heuristic (REH) [51] for MVCP and the earliest due date (EDD) dispatching rule [52] for SMTWTP. We also use the ACO (with 20 ants and 50 iterations) [38] as the metaheuristic baseline to solve the problems. The heuristics for TSP and CVRP are based on the implementation of pyCombinatorial<sup>1</sup> and VeRyPy<sup>2</sup> , respectively. 

**NCO Solvers:** We compare LNCS with other NCO approaches, including AM [39] and POMO [28], across TSP, CVRP, and KP. These methods rely on numerical features as input, enabling us to assess the current performance gap between text-attributed COP solutions and numerically based NCO methods. 

## _C. Performance Evaluation_ 

**Comparison with LLM-based Optimization.** To evaluate our method, we compare it against both _LLMs as programmers_ and _LLMs as optimizers_ approaches, which have been extensively explored in the LLM community. We center our comparison on TSP, CVRP, and KP. The results presented in Table I demonstrate that LNCS achieves the best performance among all LLM-based frameworks. 

Although existing methods can only address small-scale COPs effectively [9], their performance still remains suboptimal even on the simple TSP (with 20 nodes), suggesting that relying solely on embedded knowledge within LLMs is insufficient at the current stage. In contrast, our LNCS incorporates an additional Transformer and a specialized RL training process, allowing the integration of domain-specific knowledge of COPs. This enhancement enables LLMs to solve various COPs more effectively in a unified way. 

**Comparison with Heuristic-Based Optimization.** Given that the LNCS achieves state-of-the-art (SOTA) performance among existing LLM-based methods, we further investigate its performance relative to traditional heuristic methods. The results of the comprehensive experiments are presented in Table II, where the LNCS generally outperforms the heuristic 

> 1https://github.com/Valdecy/pyCombinatorial 

> 2https://github.com/yorak/VeRyPy 

6 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

baselines, particularly for instances where _n ∈{_ 50 _,_ 100 _}_ . These findings indicate that our approach, through additional training, effectively addresses the LLM’s limitations in solving larger COPs (i.e. instances with over 50 nodes). **Comparison with NCO.** We also compare our model with typical NCO models. The results can be found in Appendix G, where we find that LNCS still achieves satisfactory performance. 



<!-- Start of picture text -->
CVRP CVRP<br>KP<br>KP<br>T SP<br>T SP<br>MVC<br>MVC<br>SMTWTP<br>SMTWTP<br>E5 Llama3-8B<br>ST Optimal REINF. w/o Heu.<br>Llama2-7B CGERL Optimal<br>(a) (b)<br><!-- End of picture text -->

Fig. 3: Performance comparison (with _n_ = 50) of the LNCS under different settings: (a) different LLMs (b) different training algorithms. The smaller the shadow area is, the better the corresponding setting performs. 

## _D. Ablation Study_ 

**Different LLMs.** We utilize different language models for encoding TAIs, including sentence transformer (ST) [53], e5-large-v2 (E5) [54], Llama2-7b, and Llama3-8b. The normalized results are compared in Figure 3 (a). We find that performance can generally be improved with an increase in the scale of language models. An exception is that Llama2-7b outperforms Llama3-8b in all tasks, indicating that advanced LLMs do not necessarily lead to better learning outcome. **Effect of CGERL.** We train the LNCS by both CGERL and vanilla REINFORCE (REINF.), and the normalized results are compared in Figure 3 (b). LLM with RL that has undergone conflict gradient elimination generates better solutions than the original one, demonstrating the necessity for introducing effective multi-task learning methods. 

**Heuristic Information in TAI.** We also train the model with and without heuristic information in TAI, and the results are also presented in Figure 3 (b). We find that the additional information added to the prompt can further enhance model performance, particularly on tasks such as CVRP, KP, and SMTWTP, indicating that prompt engineering can also slightly improve the LNCS. 

**Synergistic Learning between Tasks.** We empirically find that the LLM has facilitated synergistic learning between different COPs, and the results are shown and analyzed in Appendix G. 

## _E. Model Generalizability_ 

Generalizability is a key advantage offered by LLMs that enables rapid adaptation to downstream tasks. To assess this 

capability, we evaluate the generalizability by fine-tuning LNCS on new tasks. 

**Fine-tuning on New COPs.** We evaluate the cross-problem transfer capability of the trained LNCS by fine-tuning it on new COPs, i.e., VRPB and MISP. We use the model trained on COPs with _n_ = 50 and fine-tune it on VRPB with _n_ = 50 (VRPB50) and MISP with _n_ = 100 (MISP100), respectively. 



<!-- Start of picture text -->
Fine-tune<br>From scratch<br>40<br>20<br>Fine-tune<br>35<br>10 From scratch<br>0 2500 5000 0 2500 5000<br>Training Step Training Step<br>(a) (b)<br>Obj. Obj.<br><!-- End of picture text -->

Fig. 4: Results by fine-tuning and learning from scratch for (a) VRPB50 and (b) MISP100. 

We randomly initialize the LNCS and train it on each task using 6,000 steps from scratch, which is taken as the baseline. In contrast, for the VRPB50 task, we employ only 2,000 steps for fine-tuning, while for the MISP100 task, the fine-tuning process follows the same number of steps as in the training from scratch. The results are shown in Figure 4. As observed, for the VRPB task, the trained LNCS already learned to solve some routing problems, such as CVRP and TSP, so that it can get better result than random initialization even in the first batch. Compared to learning from scratch, the fine-tuning on new VRP tasks brings about a faster convergence with better performance, demonstrating the few-shot generalization capability of the model. 

For the MISP task, the convergence is slower than that of learning from scratch. This is primarily because MISP and MVCP are complementary problems on any given graph. Specifically, for a graph _G_ = ( _V, E_ ), the maximum independent set is _I_ = _V/C_ , where _C_ is the maximum vertex cover of _G_ . Consequently, a neural network trained on MVCP must learn an entirely different decision-making process for MISP, leading to suboptimal performance in the initial batches. However, after approximately 2,000 steps, the fine-tuning achieves performance comparable to that of the learning-fromscratch model and eventually converges to a better result. This shows that fine-tuning on a complementary task can still be beneficial. 

**Fine-tuning on New Size.** We compare the fine-tuning and training from scratch for COPs with _n_ = 100. The results shown in Appendix G demonstrate that fine-tuning on new problem size allows rapid adaptations under few-shot setting. 

## VI. CONCLUSION 

This paper presents a framework for elevating LLMs in solving text-attributed COPs. Leveraging TAIs, the method integrates an LLM with a Transformer-based solution generator. To enable simultaneous learning across multiple tasks, a multitask RL approach is employed to address conflicting gradients 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

7 

||Method|Obj.|_n_= 20<br>Gap|Time|Obj.|_n_= 50<br>Gap|Time|Obj.|_n_= 100<br>Gap|Time|
|---|---|---|---|---|---|---|---|---|---|---|
||OR tools|3.85|0.00%|0.36s|5.87|3.07%|0.60s|8.13|4.65%|1.32s|
||Nearest neighbor|4.51|17.21%|_<_0.01s|6.98|22.72%|0.03s|9.69|24.86%|0.10s|
|_SP_|Farthest insertion|3.96|2.89%|0.21s|5.98|4.97%|4.32|8.21|5.74%|126s|
|_T_|ACO|3.94|2.23%|0.74s|6.54|14.94%|1.53s|9.99|28.74%|2.01s|
||LNCS (ours)|3.87|0.39%|0.72s|5.79|1.64%|1.64s|8.10|4.38%|3.60s|
||OR tools|6.18|1.30%|0.27s|11.05|6.63%|0.48s|17.36|12.07%|1.40s|
||Sweep heuristic|7.51|23.17%|0.01s|15.65|50.95%|0.05s|28.40|83.39%|0.25s|
|_VRP_|Parallel saving|6.33|3.85%|_<_0.01s|10.90|5.18%|_<_0.01s|16.42|6.03%|0.03s|
|_C_|ACO|7.72|26.51%|0.80s|15.76|52.12%|1.97s|26.66|72.07%|4.90s|
||LNCS (ours)|6.25|2.51%|0.90s|10.74|3.62%|2.15s|16.35|5.59%|4.80s|
||OR tools|7.948|-0.01%|_<_0.01s|20.086|-0.01%|_<_0.01s|40.377|0.00%|_<_0.01s|
|_P_|Greedy policy|7.894|0.67%|_<_0.01s|20.033|0.26%|_<_0.01s|40.328|0.12%|_<_0.01s|
|_K_|ACO|7.947|0.00%|0.72s|20.053|0.15%|2.19s|40.124|0.62%|3.41s|
||LNCS (ours)|7.939|0.10%|0.06s|20.071|0.06%|0.17s|40.361|0.03%|0.26s|
|_P_|MVCApprox|14.595|22.13%|_<_0.01s|34.856|20.98%|_<_0.01s|68.313|21.57%|_<_0.01s|
|_VC_|REH|16.876|41.22%|_<_0.01s|41.426|43.78%|_<_0.01s|81.860|45.68%|_<_0.01s|
|_M_|LNCS (ours)|12.900|7.93%|0.1s|32.101|11.42%|0.43s|64.893|15.49%|1.63s|
|_TP_|EDD|0.3822|275.81%|_<_0.01s|0.4461|107.68%|_<_0.01s|0.4434|81.87%|_<_0.01s|
|_TW_|ACO|0.2967|191.74%|0.35s|1.0471|387.48%|1.35s|6.77|2677%|2.00s|
|_SM_|LNCS (ours)|0.2862|181.41%|0.09s|0.3353|56.10%|0.31s|0.3316|36.01%|1.10s|



TABLE II: Performance on 1K instances for the COPs. Obj. indicates the average objective values. The gaps are computed using the optimal solutions produced by Gurobi. The average gaps and computation time are reported. 

during training. The proposed model demonstrates competitive performance across various COPs, surpassing all existing LLM-based optimization methods. Consequently, this work introduces a unified paradigm to enable LLMs to generate high-quality COP solutions. 

## REFERENCES 

- [1] M. T. R. Laskar, M. S. Bari, M. Rahman, M. A. H. Bhuiyan, S. Joty, and J. X. Huang, “A systematic study and comprehensive evaluation of chatgpt on benchmark datasets,” _arXiv preprint arXiv:2305.18486_ , 2023. 

- [2] C. Qian, B. He, Z. Zhuang, J. Deng, Y. Qin, X. Cong, Z. Zhang, J. Zhou, Y. Lin, Z. Liu, and M. Sun, “Tell me more! towards implicit user intention understanding of language model driven agents,” in _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics_ , Aug. 2024, pp. 1088–1113. 

- [3] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman _et al._ , “Evaluating large language models trained on code,” _arXiv preprint arXiv:2107.03374_ , 2021. 

- [4] F. Zhang, B. Chen, Y. Zhang, J. Keung, J. Liu, D. Zan, Y. Mao, J.G. Lou, and W. Chen, “RepoCoder: Repository-level code completion through iterative retrieval and generation,” in _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , Dec. 2023, pp. 2471–2484. 

- [5] C. Chen, X. Wang, T.-E. Lin, A. Lv, Y. Wu, X. Gao, J.-R. Wen, R. Yan, and Y. Li, “Masked thought: Simply masking partial reasoning steps can improve mathematical reasoning learning of language models,” in _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics_ , Aug. 2024, pp. 5872–5900. 

- [6] Y. Zhao, Y. Long, H. Liu, R. Kamoi, L. Nan, L. Chen, Y. Liu, X. Tang, R. Zhang, and A. Cohan, “DocMath-eval: Evaluating math reasoning capabilities of LLMs in understanding long and specialized documents,” in _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics_ , 2024, pp. 16 103–16 120. 

- [7] C. Blum and A. Roli, “Metaheuristics in combinatorial optimization: Overview and conceptual comparison,” _ACM Computing Surveys_ , vol. 35, no. 3, p. 268–308, sep 2003. 

- [8] Y. Bengio, A. Lodi, and A. Prouvost, “Machine learning for combinatorial optimization: a methodological tour d’horizon,” _European Journal of Operational Research_ , vol. 290, no. 2, pp. 405–421, 2021. 

- [9] C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, and X. Chen, “Large language models as optimizers,” in _The Twelfth International Conference on Learning Representations_ , 2023. 

- [10] M. Masoud, A. Abdelhay, and M. Elhenawy, “Exploring combinatorial problem solving with large language models: A case study on the travelling salesman problem using gpt-3.5 turbo,” _arXiv preprint arXiv:2405.01997_ , 2024. 

- [11] Z. Iklassov, Y. Du, F. Akimov, and M. Takac, “Self-guiding exploration for combinatorial problems,” _Advances in Neural Information Processing Systems_ , vol. 37, 2024. 

- [12] X. Xu, T. Xiao, Z. Chao, Z. Huang, C. Yang, and Y. Wang, “Can llms solve longer math word problems better?” _arXiv preprint arXiv:2405.14804_ , 2024. 

- [13] J. Yu, Y. Ren, C. Gong, J. Tan, X. Li, and X. Zhang, “Empower textattributed graphs learning with large language models (llms),” _arXiv preprint arXiv:2310.09872_ , 2023. 

- [14] A. Zolnai-Lucas, J. Boylan, C. Hokamp, and P. Ghaffari, “STAGE: Simplified text-attributed graph embeddings using pre-trained LLMs,” in _Proceedings of the 1st Workshop on Knowledge Graphs and Large Language Models (KaLLM 2024)_ , Aug. 2024, pp. 92–104. 

- [15] H. Liu, J. Feng, L. Kong, N. Liang, D. Tao, Y. Chen, and M. Zhang, “One for all: Towards training one graph model for all classification tasks,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [16] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi _et al._ , “Mathematical discoveries from program search with large language models,” _Nature_ , vol. 625, no. 7995, pp. 468–475, 2024. 

- [17] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and Q. Zhang, “Evolution of heuristics: Towards efficient automatic algorithm design using large language model,” in _International Conference on Machine Learning_ , 2024. [Online]. Available: https://arxiv.org/abs/2401.02051 

- [18] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim, J. Park, and G. Song, “Reevo: Large language models as hyper-heuristics with reflective evolution,” in _Advances in Neural Information Processing Systems_ , 2024, https://github.com/ai4co/reevo. 

- [19] Z. Xiao, D. Zhang, Y. Wu, L. Xu, Y. J. Wang, X. Han, X. Fu, T. Zhong, J. Zeng, M. Song, and G. Chen, “Chain-of-experts: When LLMs meet complex operations research problems,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/forum?id=HobyL1B9CZ 

- [20] J. Zhang, W. Wang, S. Guo, L. Wang, F. Lin, C. Yang, and W. Yin, “Solving general natural-language-description optimization problems with large language models,” in _Proceedings of the 2024 Conference_ 

BRIDGING LARGE LANGUAGE MODELS AND OPTIMIZATION: A UNIFIED FRAMEWORK FOR TEXT-ATTRIBUTED COMBINATORIAL OPTIMIZATION 

8 

   - _of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , Jun. 2024, pp. 483–490. 

- [21] S. Wasserkrug, L. Boussioux, D. d. Hertog, F. Mirzazadeh, I. Birbil, J. Kurtz, and D. Maragno, “From large language models and optimization to decision optimization copilot: A research manifesto,” _arXiv preprint arXiv:2402.16269_ , 2024. 

- [22] H. Abgaryan, A. Harutyunyan, and T. Cazenave, “LLMs can schedule,” _arXiv preprint arXiv:2408.06993_ , 2024. 

- [23] S. Liu, C. Chen, X. Qu, K. Tang, and Y.-S. Ong, “Large language models as evolutionary optimizers,” in _2024 IEEE Congress on Evolutionary Computation (CEC)_ . IEEE, 2024, pp. 1–8. 

- [24] Y. Zhang, H. Wang, S. Feng, Z. Tan, X. Han, T. He, and Y. Tsvetkov, “Can llm graph reasoning generalize beyond pattern memorization?” 2024. [Online]. Available: https://arxiv.org/abs/2406.15992 

- [25] O. Vinyals, M. Fortunato, and N. Jaitly, “Pointer networks,” _Advances in neural information processing systems_ , vol. 28, 2015. 

- [26] I. Bello, H. Pham, Q. V. Le, M. Norouzi, and S. Bengio, “Neural combinatorial optimization with reinforcement learning,” _arXiv preprint arXiv:1611.09940_ , 2016. 

- [27] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [28] Y.-D. Kwon, J. Choo, B. Kim, I. Yoon, Y. Gwon, and S. Min, “Pomo: Policy optimization with multiple optima for reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 21 188–21 198, 2020. 

- [29] M. Kim, J. Park, and J. Park, “Sym-nco: Leveraging symmetricity for neural combinatorial optimization,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 1936–1949, 2022. 

- [30] H. Fang, Z. Song, P. Weng, and Y. Ban, “Invit: A generalizable routing problem solver with invariant nested view transformer,” _arXiv preprint arXiv:2402.02317_ , 2024. 

- [31] A. Hottung, Y.-D. Kwon, and K. Tierney, “Efficient active search for combinatorial optimization problems,” in _International Conference on Learning Representations_ , 2021. 

   - [44] F. Liu, X. Lin, Q. Zhang, X. Tong, and M. Yuan, “Multi-task learning for routing problem with cross-problem zero-shot generalization,” _arXiv preprint arXiv:2402.16891_ , 2024. 

   - [45] B. Liu, X. Liu, X. Jin, P. Stone, and Q. Liu, “Conflict-averse gradient descent for multi-task learning,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 18 878–18 890, 2021. 

   - [46] T. Yu, S. Kumar, A. Gupta, S. Levine, K. Hausman, and C. Finn, “Gradient surgery for multi-task learning,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 5824–5836, 2020. 

   - [47] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale _et al._ , “Llama 2: Open foundation and fine-tuned chat models,” _arXiv preprint arXiv:2307.09288_ , 2023. 

   - [48] F. Liu, X. Tong, M. Yuan, and Q. Zhang, “Algorithm evolution using large language model,” _arXiv preprint arXiv:2311.15249_ , 2023. 

   - [49] J. Rasku, T. K¨arkk¨ainen, and N. Musliu, “Meta-survey and implementations of classical capacitated vehicle routing heuristics with reproduced results,” _Toward Automatic Customization of Vehicle Routing Systems_ , pp. 133–260, 2019. 

   - [50] R. Bar-Yehuda and S. Even, “A local-ratio theorem for approximating the weighted vertex cover problem,” in _North-Holland Mathematics Studies_ . Elsevier, 1985, vol. 109, pp. 27–45. 

   - [51] L. B. Pitt, _A simple probabilistic approximation algorithm for vertex cover_ . Yale University, Department of Computer Science, 1985. 

   - [52] J. R. Jackson, “Scheduling a production line to minimize maximum tardiness,” _Management science research project_ , 1955. 

   - [53] N. Reimers and I. Gurevych, “Sentence-bert: Sentence embeddings using siamese bert-networks,” in _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLPIJCNLP)_ , 2019, pp. 3982–3992. 

   - [54] L. Wang, N. Yang, X. Huang, B. Jiao, L. Yang, D. Jiang, R. Majumder, and F. Wei, “Text embeddings by weakly-supervised contrastive pretraining,” _arXiv preprint arXiv:2212.03533_ , 2022. 

- [32] R. Qiu, Z. Sun, and Y. Yang, “Dimes: A differentiable meta solver for combinatorial optimization problems,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 25 531–25 546, 2022. 

- [33] J. Choo, Y.-D. Kwon, J. Kim, J. Jae, A. Hottung, K. Tierney, and Y. Gwon, “Simulation-guided beam search for neural combinatorial optimization,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 8760–8772, 2022. 

- [34] Y. Wu, W. Song, Z. Cao, J. Zhang, and A. Lim, “Learning improvement heuristics for solving routing problems,” _IEEE Transactions on Neural Networks and Learning Systems_ , vol. 33, no. 9, pp. 5057–5069, 2022. 

- [35] B. Hudson, Q. Li, M. Malencia, and A. Prorok, “Graph neural network guided local search for the traveling salesperson problem,” in _International Conference on Learning Representations_ , 2021. 

- [36] Y. Ma, J. Li, Z. Cao, W. Song, H. Guo, Y. Gong, and Y. M. Chee, “Efficient neural neighborhood search for pickup and delivery problems,” in _International Joint Conference on Artificial Intelligence_ , 2022, pp. 4776–4784. 

- [37] S. Li, Z. Yan, and C. Wu, “Learning to delegate for large-scale vehicle routing,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 26 198–26 211, 2021. 

- [38] H. Ye, J. Wang, Z. Cao, H. Liang, and Y. Li, “Deepaco: Neuralenhanced ant systems for combinatorial optimization,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [39] W. Kool, H. van Hoof, and M. Welling, “Attention, learn to solve routing problems!” in _International Conference on Learning Representations_ , 2018. 

- [40] J. Zhou, Y. Wu, W. Song, Z. Cao, and J. Zhang, “Towards omnigeneralizable neural methods for vehicle routing problems,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 42 769– 42 789. 

- [41] R. J. Williams, “Simple statistical gradient-following algorithms for connectionist reinforcement learning,” _Machine learning_ , vol. 8, pp. 229–256, 1992. 

- [42] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ , 2016. 

- [43] S. Ioffe and C. Szegedy, “Batch normalization: Accelerating deep network training by reducing internal covariate shift,” in _International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 37. PMLR, 2015, pp. 448–456. 

