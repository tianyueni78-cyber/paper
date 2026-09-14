# **Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models** 

Xuan Wu Di Wang College of Computer Science and LILY Research Centre, Nanyang Technology, Jilin University Technological University Changchun, Jilin, China Singapore wuuu22@mails.jlu.edu.cn wangdi@ntu.edu.sg 

Lijie Wen Chunyan Miao School of Software, Tsinghua LILY Research Centre, Nanyang University Technological University Beijing, China Singapore wenlj@tsinghua.edu.cn ascymiao@ntu.edu.sg 

Chunguo Wu Key Laboratory of Symbolic Computation and Knowledge Engineering of Ministry of Education, Jilin University Changchun, Jilin, China wucg@jlu.edu.cn 

Yubin Xiao<sup>∗</sup> College of Computer Science and Technology, Jilin University Changchun, Jilin, China xiaoyb21@mails.jlu.edu.cn 

You Zhou<sup>∗</sup> 

College of Software, Jilin University Changchun, Jilin, China zyou@jlu.edu.cn 

## **Abstract** 

Recent studies exploited Large Language Models (LLMs) to autonomously generate heuristics for solving Combinatorial Optimization Problems (COPs), by prompting LLMs to first provide search directions and then derive heuristics accordingly. However, the absence of task-specific knowledge in prompts often leads LLMs to provide unspecific search directions, obstructing the derivation of well-performing heuristics. Moreover, evaluating the derived heuristics remains resource-intensive, especially for those semantically equivalent ones, often requiring omissible resource expenditure. To enable LLMs to provide specific search directions, we propose the Hercules algorithm, which leverages our designed Core Abstraction Prompting (CAP) method to abstract the core components from elite heuristics and incorporate them as prior knowledge in prompts. We theoretically prove the effectiveness of CAP in reducing unspecificity and provide empirical results in this work. To reduce computing resources required for evaluating the derived heuristics, we propose few-shot Performance Prediction Prompting (PPP), a first-of-its-kind method for the Heuristic Generation (HG) task. PPP leverages LLMs to predict the fitness values of newly derived heuristics by analyzing their semantic similarity to previously evaluated ones. We further develop two tailored 

∗Corresponding Authors. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _KDD ’25, August 3–7, 2025, Toronto, ON, Canada_ 

© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-1454-2/2025/08 https://doi.org/10.1145/3711896.3736923 

mechanisms for PPP to enhance predictive accuracy and determine unreliable predictions, respectively. The use of PPP makes Hercules more resource-efficient and we name this variant Hercules-P. Extensive experiments across four HG tasks, five COPs, and eight LLMs demonstrate that Hercules outperforms the state-of-the-art LLM-based HG algorithms, while Hercules-P excels at minimizing required computing resources. In addition, we illustrate the effectiveness of CAP, PPP, and the other proposed mechanisms by conducting relevant ablation studies. 

## **CCS Concepts** 

- **Mathematics of computing** → **Combinatorial optimization** ; 

- **Computing methodologies** → **Search methodologies** . 

## **Keywords** 

Large Language Models; Heuristic Generation; Combinatorial Optimization Problems 

#### **ACM Reference Format:** 

Xuan Wu, Di Wang, Chunguo Wu, Lijie Wen, Chunyan Miao, Yubin Xiao, and You Zhou. 2025. Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models. In _Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 (KDD ’25), August 3–7, 2025, Toronto, ON, Canada._ ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3711896.3736923 

**KDD Availability Link:** 

The source code of this paper has been made publicly available at https: //doi.org/10.5281/zenodo.15462797. 

## **1 Introduction** 

Heuristic algorithms have long been a preferred approach for solving Combinatorial Optimization Problems (COPs) [33, 43]. To automate the derivation of heuristics for a given COP, Heuristic Generation (HG) methods have attracted significant attention [5]. Early 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 



<!-- Start of picture text -->
(a) Search directions produced using RP<br>Below are two [function_name] functions for [problem], where the<br>second version performs better than the first one. [Worse code]<br>[Better code]. You respond with some hints for designing better<br>heuristics.<br>Understand problem specifics,  favor shorter paths, avoid zero<br>division, normalize heuristic values,  test and iterate .<br>(b) Search directions produced using CAP<br>The [function_name] is a part of [algorithm] for solving [problem].<br>Summarize the core components of these functions that potentially<br>influence the performance of the algorithm: [code][code][code] .<br>Core components: 1. Penalty Calculation: The approaches employ<br>varying strategies to calculate penalties or desirability, such as<br>using ratios of distances, normalizing values. 2. …<br>Below are two functions. The second version performs better than<br>the first one. [Worse code][Better code]. Below are some components<br>of functions. [components] Reflect on why the second performs<br>better than the first, considering components.<br>Normalize penalties relative to overall distance.<br><!-- End of picture text -->

**Figure 1: Illustration of the search directions produced using RP [53] and CAP (our method) for the task described in Section 4.1. When RP prompts LLMs (GPT-4o-mini used in this example) for search directions directly, the LLMs may respond with unspecific search directions (highlighted in yellow). Different from RP, CAP enhances the quality of the produced search directions by first prompting the LLMs to abstract the core components of elite heuristics as prior knowledge in a zero-shot manner (highlighted in purple).** 

HG methods predominantly employ Evolutionary Computation (EC) to derive heuristics. However, these methods focus on the exploration and exploitation in the micro search space composed of the predefined modules, resulting in limited performance [53]. 

Recently, the emergence of Large Language Models (LLMs) has facilitated the autonomous derivation of heuristics, eliminating the need for manually defining the search space [22, 23, 37]. In addition, compared to conventional EC algorithms, LLMs benefit from a broader search space by leveraging their mega-size training corpora, resulting in elevated performance [25, 29, 52]. Specifically, these LLM-based HG methods exploit LLMs to provide search directions, which are then used to derive (novel) offspring heuristics [35]. These produced heuristics are subsequently evaluated using COP instances to determine their fitness values, with the betterperforming heuristics carried over to the next iteration. For example, Liu et al. [23] proposed prompting methods that emulate crossover and mutation operators as search strategies, thereby implicitly providing search directions. To let LLMs offer more explicit search directions, Ye et al. [53] proposed Reflection Prompting (RP), which requires LLMs to reflect on the relative performance of the produced heuristics and provide insights as search directions. These directions are then used to derive heuristics with expected elevated performance in subsequent crossover and mutation promptings. 

These existing LLM-based HG methods face two key challenges. Firstly, when prompting LLMs to provide search directions (e.g., reflections on the relative performance of heuristics), the lack of taskspecific knowledge in prompts often leads to over-generalized, unspecific directions that hinder the derivation of high-performance heuristics. As illustrated in Figure 1(a), the produced search directions _“Understand problem specifics"_ and _“test and iterate"_ are vague, over-general, and lack actionable steps required for heuristic generation. Consequently, they contribute little to the derivation of high-performance heuristics. In contrast, other elements of the produced search directions are more specific. For example, _“normalize_ 



<!-- Start of picture text -->
def select_next_node (current_node :  def select_next_node (current_node :<br>int , destination_node:  int , int , destination_node:  int ,<br>unvisited_nodes:  set , unvisited_nodes:  set , distance_matrix:<br>distance_matrix: np.ndarray)  - > int : np.ndarray)  -> int :<br>c1, c2, c3, c4 =  0.4 ,  0.3 ,  0.2 , 0.1 c1, c2, c3, c4 =  0.4 ,  0.3 ,  0.2 ,  0.1<br>scores = {} scores = {}<br>for node  i n unvisited_nodes: for node  i n unvisited_nodes:<br>other_nodes =  list (unvisited_nodes  other_nodes =  list (unvisited_nodes -<br>- {node} ) {node} )<br>mean_distance = np.mean mean_distance = np.mean<br>(distance_matrix[node,other_node] ) (distance_matrix[node,other_nodes] )<br>std_distance = np.std std_distance = np.std<br>(distance_matrix[node, other_nodes] ) (distance_matrix[node, other_nodes] )<br>lookahead_score = c1*  distance = distance_matrix<br>distance_matrix[current_node] [ node]  - [destination_node][node]<br>c2* mean_distance + c3* std_distance – lookahead_score = c1*<br>c4* distance_matrix distance_matrix[current_node][node] –<br>[ destination_node] [ node] c2* mean_distance + c3* std_distance -<br>scores[node] = lookahead_score c4* distance<br>next_node = min (scores, key =scores. scores[node] = lookahead_score<br>get) next_node = min (scores, key =scores.<br>return next_node (a) get) return next_node (b)<br><!-- End of picture text -->

**Figure 2: Illustration of two heuristics with identical semantics, produced by RP [53] (GPT-3.5-turbo used in this example) for the task described in Section 4.2. Code snippets with literal equivalence are highlighted in blue, while those with semantic equivalence are highlighted in pink.** 

_heuristic values"_ provides an actionable step that can be directly applied to derive heuristics. Therefore, it is essential to reduce unspecificity in the produced search directions. Secondly, during the search process, LLM-based HG methods often derive numerous heuristics, some of which may be semantically or even literally identical, as illustrated in Figure 2. Reevaluating these heuristics using COP instances (i.e., conventional fitness evaluation method) not only wastes computing resources but also significantly prolongs the search process [6]. In particular, these heuristics often involve numerous linear operations and conditional branches, which GPUs cannot efficiently accelerate [38]. In addition, providing LLMs with all historical heuristics to avoid deriving semantically similar ones is impractical. This approach may compel LLMs to derive overly random or unviable heuristics, while significantly increasing the cost of context tokens. 

To better address the first challenge, we propose **He** u **r** isti **c** Generation **U** sing **L** arge Languag **e** Model **s** ( **Hercules** ), which exploits our proprietary, straightforward yet effective Core Abstraction Prompting ( **CAP** ) method to reduce unspecificity in the produced search directions and thus enable the derivation of high-performance heuristics. Specifically, CAP directs an LLM to abstract the core components from the top- _𝑘_ heuristics (i,e., elite heuristics) in the current population and then provide more specific search directions based on these components (see Section 3.1). Notably, as illustrated in Figure 1(b), CAP operates in a zero-shot manner, abstracting the core components without providing any examples to guide this abstraction process, which leads to significant savings in context token costs. Meanwhile, by incorporating the concept of information gain, we theoretically prove that CAP can reduce unspecificity in the produced search directions in Appendix A. To couple with CAP, we introduce a rank-based selection mechanism that increases the likelihood of selecting high-performance heuristics as parents (used in the following crossover and mutation promptings), rather than relying on random selection [53]. 

To better address the second challenge, we propose **Hercules-P** , which integrates CAP with our novel Performance Prediction Prompting ( **PPP** ) method. PPP operates in a few-shot manner by presenting LLMs with a small set of previously evaluated heuristics as 

Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

examples and prompting LLMs to predict the fitness values of the newly produced heuristics based on their semantic similarity to the presented examples (see Section 3.2). Therefore, PPP reduces the number of heuristics that require evaluation using COP instances. Generally speaking, to enhance the predictive accuracy of PPP, we can either increase the number of examples or enhance their quality. However, collecting numerous heuristic examples along with their corresponding performance is resource-intensive. This contradicts to the primary purpose of incorporating PPP, which is to reduce resource expenditure during the search process. Moreover, unlike Neural Architecture Search (NAS), which benefits from extensive benchmarks [32, 44, 54], the HG task lacks benchmarks with pre-evaluated heuristics. Therefore, we opt to provide higherquality examples through a tailored example selection mechanism, termed EXEMPLAR, which favors distinct parent heuristics with superior performance as examples. Meanwhile, to determine unreliable predictions, we develop the Confidence Stratification (ConS) mechanism that requires the LLM to provide confidence levels for the predicted fitness values, thereby facilitating the identification of heuristics that need reevaluation. In summary, PPP reduces the resource expenditure in heuristic evaluations while maintaining population diversity, making it effective for tasks with a border search space. To the best of our knowledge, **our work proposes the first LLM-based performance predictor for the HG task.** 

To assess the performance of the proposed Hercules and HerculesP algorithms, we conduct extensive experiments on four HG tasks (see Section 4). The experimental results demonstrate that Hercules outperforms the state-of-the-art (SOTA) LLM-based HG algorithms across four HG tasks, five COPs, and eight LLMs, without significantly increasing context or generation token costs. By incorporating PPP, Hercules-P significantly reduces the overall search time by 7%∼59% when compared to Hercules, while achieving on-par performance on the gain metric. Finally, ablation studies validate the effectiveness of the proposed EXEMPLAR and ConS methods. 

The key contributions of this work are as follows. 

**i)** We propose the zero-shot CAP method, which reduces unspecificity in the LLM-produced search directions, enabling the derivation of high-performance heuristics. We also provide theoretical proof of CAP’s effectiveness in reducing unspecificity by utilizing the concept of information gain. 

**ii)** We propose the few-shot PPP method, a first-of-its-kind LLMbased performance predictor specifically designed for HG tasks. PPP predicts the performance of newly produced heuristics by analyzing their semantic similarity to previously evaluated ones. Moreover, we develop two novel mechanisms: EXEMPLAR and ConS, which significantly enhance the overall performance of PPP. 

**iii)** The experimental results demonstrate that our proposed Hercules achieves SOTA performance across four HG tasks, five COPs, and eight LLMs, while Hercules-P excels at reducing resource expenditure. Finally, ablation study results validate the effectiveness of all proposed methods. 

## **2 Related Work** 

In this section, we review the relevant literature. 

## **2.1 LLM-based Heuristic Generation Algorithms** 

Conventional EC-based HG algorithms search for the optimal combination of the predefined heuristic modules [17], which often limits 

their performance. In contrast, LLM-based HG algorithms eliminate the need for predefining the search space, liberating researchers from manual customization and enabling the derivation of highperformance heuristics [14, 46]. Specifically, these algorithms begin with a seed heuristic to prompt LLMs to derive multiple heuristics as the initial population [22, 23, 53]. Each heuristic is then evaluated using a set of COP instances, with its performance serving as its fitness value. During the iterative process, certain heuristics are selected as parents and presented to LLMs to derive (novel) offspring heuristics. This approach emulates the concepts of crossover and mutation, while implicitly providing search directions for the LLMs to derive heuristics. In addition, certain studies exploit LLMs to provide explicit search directions for deriving well-performing heuristics [53]. However, these LLM-based HG algorithms overlook the issue of unspecificity in LLM responses (see Figure 1(a)), which can lead to unspecific search directions that do not contribute to discovering high-performance heuristics. 

Similar challenges are observed in tasks such as arithmetic and symbolic reasoning, making it crucial to evoke LLM reasoning through a multi-step process and incorporate task-specific knowledge [16, 28, 55]. For example, Wei et al. [41] proposed Chain-ofThought (CoT) prompting, which directs LLMs to emulate the given examples in completing a multi-step solution process, leading to more accurate answers. Subsequently, Zheng et al. [58] proposed the few-shot Step-back Prompting (SP), which exploits the given examples to enable LLMs to abstract high-level principles and then apply these principles in reasoning. In a similar multi-step fashion, we propose CAP to mitigate unspecificity in the produced search directions for better solving HG tasks. However, unlike CoT and SP, CAP operates in a zero-shot manner, by abstracting the core components without any examples to guide the abstraction process. 

## **2.2 LLM-based Performance Prediction Methods** 

In the field of NAS, performance predictors, typically Deep Neural Networks, are widely used to reduce search costs by predicting the performance of candidate architectures [2, 42]. These predictors model neural architectures as graphs, where nodes represent subnets and edges represent the connections between subnets [7, 26]. The graphs are then encoded into vectors, and the mapping between these vectors and the corresponding performance metrics is learned. Recently, Chen et al. [6] and Jawahar et al. [15] proposed LLM-based predictors for predicting the performance of neural architectures. Specifically, they employed examples of architectures and corresponding performance metrics to prompt LLMs, leveraging semantic similarity to predict the performance of newly searched architectures. 

In the context of HG, conventional performance predictors may struggle to accurately evaluate heuristics due to the difficulty in modeling these diverse and complex heuristics as graph structures. However, the LLM-based predictor presents a promising alternative by eliminating the need for explicit heuristic modeling. Consequently, this paper leverages LLMs to predict the performance of heuristics for effectively solving HG tasks. However, unlike [6] and [15], which relied on a larger number of examples, our PPP emphasizes the use of only the higher-quality examples to improve predictive performance (see Section 3.2 for more details). 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 



<!-- Start of picture text -->
Legend<br>Iterative Optimization<br>ConS Heuristic Hercules<br>Crossover<br>Direction Hercules-P<br>Evaluation<br>Prediction<br>Initiation Selection EXEMPLAR CAP Mutation PPP COP instances Operator involving LLMs<br><!-- End of picture text -->

**Figure 3: Overview of the proposed Hercules and Hercules-P algorithms. Hercules exploits CAP to provide specific search directions, which are then used to guide LLMs in deriving high-performance heuristics. In Hercules, the performance of all derived heuristics on a set of COP instances determines their respective fitness values. In contrast, Hercules-P evaluates only a subset of the produced heuristics with COP instances, while the rest are assessed using the proposed PPP method.** 

## **2.3 Neural Combinatorial Optimization Solvers** 

Neural Combinatorial Optimization (NCO) refers to a class of Neural Network solvers that either independently solve COPs or collaborate with heuristic algorithms [3, 4, 45, 47]. To enable the derivation of insights from historical COP instances and efficiently handle batches of instances in parallel, researchers have recently developed numerous NCO solvers [21, 48]. However, these NCO solvers still face several challenges. Two of the most prominent ones are how to improve their generalization capabilities [49, 59] and their performance on large-scale COPs [12, 36, 39]. Recently, Wang et al. [40] proposed a distance-aware heuristic algorithm designed to enhance the generalization ability of NCO solvers trained on small-scale COPs for solving large-scale COPs. To assess the effectiveness of the proposed Hercules and Hercules-P algorithms, we apply them to improve the performance of two classic NCO solvers on both small-scale and large-scale COPs in Section 4.4. 

## **3 Hercules and Hercules-P** 

The illustrations of Hercules and Hercules-P are schematically presented in Figure 3. In this section, we first introduce CAP, which is designed to provide more specific search directions for deriving heuristics. We then prove that CAP can reduce unspecificity of the produced search directions. Finally, we present the design of PPP, along with tailored EXEMPLAR and ConS mechanisms. 

## **3.1 Core Abstraction Prompting (CAP)** 

As aforementioned, when LLMs are tasked with providing search directions, they often generate directions that lack specificity for heuristic derivation. As illustrated in the RP example in Figure 1(a), certain directions, such as _“Understand problem specifics"_ and _“test and iterate"_ , lack relevance to heuristic derivation and fail to derive well-performing heuristics. 

In this case and many others, providing prior knowledge in prompts can help LLMs reduce unspecificity in their responses, leading to more focused, specific search directions. To achieve this, we propose the zero-shot CAP method, which can abstract the core components from the top- _𝑘_ heuristics in the current population without additional guidance. Because the core components are essential for heuristic performance [22, 51], leveraging them enables LLMs to provide more specific search directions. As shown in Figure 1(b), the suggested direction _“Normalize penalties relative to overall distance"_ may lead to more effective heuristic generation. In addition, CAP abstracts the core components once per iteration, instead of abstracting distinct components separately for crossover and elitist mutation operators. Consequently, this approach helps 

prevent a significant increase in context and generation token costs compared to RP (see Table 2 in the experiment section). 

In the field of information theory, the advantage of CAP can be quantified using the concept of information gain. Hu et al. [13] defined information gain as the reduction in entropy between two states. Extending this concept, we use information gain to quantify entropy reduction in scenarios with and without abstraction, facilitating the assessment of CAP in reducing unspecificity. Specifically, the entropy without abstraction (i.e., the core components are not presented to LLMs) in the _𝑡_ th iteration is defined as follows: 



where _𝜔𝑖_ denotes a direction belonging to the <mark>se</mark> t of al <mark>l p</mark> ossible directions Ω _𝑡_ . 

When the core components are used as prior knowledge in prompts, an LLM can provide more specific, subdivided search directions either based on one of these core components or disregarding all core components. Consequently, the set of all possible directions, Ω _𝑡_ , can be partitioned into mutually exclusive subsets, Ω _𝑗_ , where<sup>�</sup><sup>_𝑘_</sup> _𝑗_ =0<sup>Ω</sup><sup>_𝑗_=Ω</sup><sup>_𝑡_.Here,when</sup><sup>_𝑗_∈{0</sup><sup>_,_1</sup><sup>_, . . . ,𝑘_−1},Ω</sup><sup>_𝑗_</sup> denotes the subset of directions associated with the _𝑗_ th core component (for simplicity, we assume a one-to-one correspondence between core components and heuristics), while _𝑗_ = _𝑘_ corresponds to the subset of directions independent of any core component. 

Assuming that the produced direction belongs to the _𝑗_ th subset ( _𝑗_ ∈{0 _,_ 1 _, . . . ,𝑘_ }) after providing the core components, the remaining entropy is defined as follows: 



Then, the entropy with abstraction (i.e., the expected remaining entropy) is defined as<sup>�</sup><sup>_𝑘_</sup> _𝑗_ =0<sup>_𝑝𝑗𝐻_(Ω</sup><sup>_𝑗_), where</sup><sup>_𝑝𝑗_denotes the prob-</sup> ability that the search direction belongs to the _𝑗_ th subset, i.e., _𝑝 𝑗_ = _𝑝_ (Ω _𝑗_ )/ _𝑝_ (Ω _𝑡_ ). Thus, the information gain from abstracting the core components in the _𝑡_ th iteration (the entropy reduction without and with abstraction) is defined as follows: 



As proven in Appendix A, Eq. (3) simplifies to the following expression, whose value ranges within the (0 _,_ log ( _𝑘_ + 1)] interval: 



Therefore, in theory, providing the core components as prior knowledge in prompts can reduce unspecificity in LLM responses and 

Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

|`Here are some example codes and their corresponding performance`<br>`scores that you can refer to for prediction: [example_A,`<br> <br>**PPP**|
|---|
|`score_A],. . ., [example_B, score_B]. Here is a code that you need`<br>`to predict: [code].`|
|`Predict the performance of the given code bycomparing its semantic`|
|`meaning with the provided example codes.In addition,provide a`|
|`confidence level for this code, indicating the degree of semantic`<br>`similarity to the most relevant example code.The performance score`|
|`should be a float withinthe range [score_A, score_B], the`<br>`confidence number should be a float within the range [0,1].`|
|`[score=10.75, confidence=0.8]`|



**Figure 4: Illustration of the prediction process using the proposed PPP method. By analyzing the semantic similarity between the heuristics to be predicted and the previously evaluated ones, LLMs can respond with a performance score for each heuristic with an associated confidence level.** yield more specific search directions, subsequently leading to heuristics with higher performance. 

To fine-search the space with high-quality heuristics, we adopt a rank-based selection mechanism. Specifically, the probability of selecting the _𝑖_ th heuristic as a parent is computed as follows: 



where _𝑁_ denotes the population size, and rank(·) returns the rank of the associated fitness value in the ascending order. In addition, Hercules adopts the core components of the top- _𝑘_ heuristics as prior knowledge during the first _𝜆_ percent of iterations ( _𝜆_ ∈ [0,1]). In the later iterations, following [56, 57], to better preserve population diversity, Hercules directly applies the core components of the parent heuristics as prior knowledge to provide search directions, bypassing the abstraction process of elite heuristics. 

## **3.2 Performance Prediction Prompting (PPP)** 

Semantic features have demonstrated significant merits in software engineering tasks, e.g., identifying the defective code regions [24], due to their influence on the overall code performance. Motivated by this concept, we propose the few-shot PPP method, which leverages LLMs to predict the performance of newly produced heuristics by analyzing their semantic similarity to previously evaluated ones, as shown in Figure 4. To achieve higher predictive accuracy with a small number of _𝑁𝑒_ examples, we propose an example selection mechanism called EXEMPLAR, which operates on a principle similar to providing a more relevant, well-defined knowledge base in retrieval-augmented generation [10]. Specifically, EXEMPLAR selects the historically best and worst heuristics, i.e., _𝑥𝑙𝑏_ and _𝑥𝑢𝑏_ , respectively, as prediction boundaries (assuming the goal of the HG task is to derive the heuristic with the minimum fitness value), while prioritizing parent heuristics with better performance (i.e., lower fitness value). Parent heuristics with better performance are typically more complex and richer in semantic features than those with inferior performance, highly likely leading to higher prediction accuracy. In addition, any heuristic with the same fitness value as a previously selected example will not be chosen as an example. Because if LLMs encounter multiple examples sharing the same fitness value, their predictions may become biased towards this common fitness value, potentially overlooking semantic features. If each example has a distinct fitness value, LLMs can more effectively leverage semantic features to predict the performance of the new 

heuristics. The set of examples P _𝑒_ is selected as follows: 



where P _ℎ_ and P _𝑝_ denote the set of all historical heuristics and the set of parent heuristics selected from the current iteration according to Eq. (5) to produce offspring, respectively, and _𝑓_ (·) denotes the fitness evaluation function, introduced in the following paragraph. EXEMPLAR selects the set P _𝑒_ for each iteration. 

Nevertheless, LLMs cannot always accurately predict the performance of each heuristic. To mitigate the potential impact of incorrect predictions, we propose the Confidence Stratification (ConS) mechanism. Other than the LLM-predicted fitness value _𝜉𝑖_ , ConS prompts an LLM to provide a corresponding confidence level _𝜙𝑖_ ∈[0 _,_ 1] based on the degree of semantic similarity between _𝑥𝑖_ and the most similar examples in P _𝑒_ . Subsequently, based on _𝜙𝑖_ , ConS selectively accepts the predicted fitness values of certain heuristics, while others are reevaluated using COP instances. Intuitively, we implement the following design. For heuristic _𝑥𝑖_ , if _𝜙𝑖_ is sufficiently high, ConS deems _𝜉𝑖_ accurate. If _𝜙𝑖_ is moderately high, only the top-ranked candidates in this category should be trusted to directly adopt _𝜉𝑖_ without reevaluation, reflecting the degraded confidence level. For low _𝜙𝑖_ values, they can only be directly adopted if _𝜉𝑖_ is greater than a predetermined threshold. Because for these heuristics with an acceptable yet sub-par performance score and a not-too-low confidence level, it is intuitive to deem them having inferior performance, without the need for precise predictions [50]. Specifically, we heuristically define this threshold by gauging the known prediction boundaries, i.e., _𝑙𝑏𝑡_ and _𝑢𝑏𝑡_ . When _𝜙𝑖_ is extremely low, _𝜉𝑖_ is deemed unreliable and the corresponding heuristic must be reevaluated. Such design is implemented as follows to define the fitness function _𝑓_ ( _𝑥𝑖_ ): 



where _𝛿_ ∈[0 _,_ 1/3] denotes a predefined interval to distinguish the performance range of the produced heuristics (a smaller _𝛿_ value means ConS only accepts the predicted scores with the highest confidence), P _𝑐_ denotes the set of heuristics whose _𝜙𝑖_ values lie within the [1−2 _𝛿,_ 1− _𝛿_ ) interval, and F (·) denotes the conventional fitness evaluation function, which uses COP instances to evaluate heuristics. Furthermore, we gradually decrease the number of heuristics that do not require reevaluation in P _𝑐_ after each iteration. Specifically, we set an acceptance threshold _𝑚𝑡_ = ⌊ _𝛼_ · _𝛽_<sup>_𝑡_</sup> · _𝑁𝑜_ ⌋, where _𝛼_ , _𝛽_ ∈(0 _,_ 1), and _𝑁𝑜_ denotes the number of the produced heuristics in the current iteration. 

The pseudocode of Hercules-P is presented in Algorithm 1, and its code is available online (https://github.com/wuuu110/Hercules). The details about the adopted crossover and elitist mutation operators, along with other EC definitions, are presented in Appendix B. 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 

**Table 1: Performance comparison of different GLS algorithms on TSP** 

|Algorithm|LLM: Lla<br>|ma3-70b<br>|LLM: GP<br>|T-4o-mini<br>|
|---|---|---|---|---|
||Gain (%) (_𝑛_=100)|Gain (%) (_𝑛_=200)|Gain (%) (_𝑛_=100)|Gain (%) (_𝑛_=200)|
|KGLS-Random|-137.13|0.47|63.64|3.44|
|KGLS-EoH (ICML’24)|-369.10|5.82|25.53|5.62|
|KGLS-ReEvo (NeurIPS’24)|-661.69|2.19|-280.79|2.45|
|KGLS-Hercules-P (ours)|-218.91|4.71|**71.05**|7.46|
|KGLS-Hercules (ours)|-12.48|3.42|42.98|**11.10**|
|**Algorithm 1**Hercules-P for DerivingHeur<br>**Input**: Maximum iteration number_𝑇_|istics|**Table 2: S    f**<br>**algorithm**|**earch cost compa  f**<br>**s on TSP**|**rison of differen**|
|**Output**: Best heuristic_𝑥best_<br>1: Initialize and evaluate populationP||Alg<br>|orithm<br>Gain<br><br>|(%)<br>Time (m)<br>Co<br>To<br><br><br>|



**Table 2: Search cost comparison of different LLM-based HG algorithms on TSP** 

|Algorithm|Gain (%)|Time (m)|Context<br>Token (k)|Generation<br>Token (k)|G|
|---|---|---|---|---|---|
|KGLS-Random|3.44±1.20|28.5<br>±2.2|**0.2**|**19.4**|PT-|
|KGLS-EoH (ICML’24)|5.62±1.83|37.2±7.2|43.5|26.2|4o|
|KGLS-ReEvo (NeurIPS’24)|2.45±10.93|37.7±12.2|95.5|42.0|-m|
|KGLS-Hercules-P (ours)|7.46<br>±5.36|**23.6**±3.0|143.4|31.2|ini|
|KGLS-Hercules (ours)|**11.10**±0.69|30.6±1.4|95.8|33.3||



- # Omitting Steps 4, 12, and 13 makes Hercules-P fall back to the original Hercules algorithm 

- 2: **for** iteration _𝑡_ = 0 to _𝑇_ **do** 3: Select parents set P _𝑝_ via Eq. (5) _//Rank-based selection_ 4: Select examples set P _𝑒_ for PPP via Eq. (6) _//EXEMPLAR_ 

**Table 3: Performance comparison of different constructive heuristic algorithms on TSPLIB** 

- 5: **if** _𝑡_ ≤ _𝜆_ · _𝑇_ **then** 

- 6: Provide search directions using core components of elite heuristics _//CAP_ 

|instances|Random|EoH|ReEvo|Hercules-P|Hercules||
|---|---|---|---|---|---|---|
|(total number)||(ICML’24)|(NeurIPS’24)|(ours)|(ours)|GP|
|_𝑛<_101(4)|-3.92|**16.68**|1.18|14.16|10.52|T-3.|
|101 ≤_𝑛_≤500(9)|-3.80|-0.60|-1.17|0.71|**2.25**|5-t|
|_𝑛>_500(5)|-5.73|**5.32**|0.46|0.95|5.18|urb|
|Avg. Gain (%) (18)|-4.49|4.80|-0.16|3.42|**4.87**|o|



- 7: **else** 

- 8: Provide search directions using core components of parent heuristics 

- 9: **end if** 

- 10: Derive heuristics using crossover based on the produced search directions 

produced by these algorithms are presented in Table 1, where _𝑛_ denotes the problem scale. The gain measure is calculated as 1-(the performance of the LLM-produced heuristics)/(the performance of the original KGLS). 

- 11: Derive heuristics using elitist mutation based on the produced search directions 

As shown in Table 1, for the 200-node TSP, the heuristics produced by Hercules using GPT-4o-mini outperform those produced by the other HG algorithms, yielding the best performance gain of 11.1%. In addition, when GPT-4o-mini is adopted, the average gain of Hercules-P drops by only 3.64% comparing to Hercules, securing the second-best performance. EoH ranks at the third place in the gain metric. The experimental results shown in Table 1 highlight that the choice of LLM significantly impacts the performance of the produced heuristics. Nevertheless, Hercules and Hercules-P consistently outperform ReEvo across all node scales, regardless of the LLM in use. In addition, to better illustrate the improvement achieved by adopting Hercules, we present a real-wolrd case study on optimizing a travel route to visit all U.S. state capitals in Appendix E.1. The results of the showcased case study highlight the substantial practical values of Hercules, offering a travel route that reduces the total travel distance by nearly 200 miles compared to those provided by other LLM-derived algorithms (yielding an improvement of 1.69% in the gain metric over the second-best method). 

- 12: Predict fitness of the newly produced heuristics _//PPP_ 13: Determine fitness values _𝑓_ (·) via Eq. (7) _//ConS_ 14: Update P and _𝑥best_ with new heuristics 15: **end for** 

## **4 Experimental Results** 

This section presents extensive experimental results on various HG tasks, COPs, and LLMs to assess the performance of both Hercules and Hercules-P. Please refer to Appendices C to G for the experimental setups with predefined hyperparameter values, prompts used in this paper, additional experimental results, comparative examples of search directions produced by RP and CAP, and the produced heuristics, respectively. 

## **4.1 Deriving GLS Heuristics to Solve TSP** 

In this subsection, we exploit Hercules and Hercules-P to derive penalty heuristics for Guided Local Search (GLS) to solve the Travelling Salesman Problem (TSP). The seed function is human-designed heuristic KGLS [1]. We choose three LLM-based HG algorithms as benchmarking models, namely Random, EoH [22], and ReEvo [53]. Random is a straightforward method that derives heuristics directly using LLMs without incorporating search directions and is commonly used as a baseline model in NAS studies [20]. In addition, unless specified otherwise, for the performance of LLM-based HG algorithms, namely Random, EoH, ReEvo, Hercules-P, and Hercules, we report the average performance of three independent runs, following the prior study [53]. The average gains of the heuristics 

Table 2 presents the search cost comparison of LLM-based HG algorithms across four metrics, namely gain (identical to the bottomright cell of Table 1), search time, context token, and generation token. The results show that Hercules yields better gains without substantially increasing the costs of context and generation tokens, compared to ReEvo. Moreover, ReEvo and EoH spend longer search time when compared to the others, likely due to their ineffective search directions, which cause the LLM to derive complex but suboptimal heuristics. The std value of 10.93 for ReEvo further 

Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

**Table 4: Performance comparison of different ACO algorithms on BPP and MKP** 

|Algorithm|Type|BPP (Gain<br>_𝑛_=120|(%)), LLM: Lla<br>_𝑛_=500|ma3.1-405b<br>_𝑛_=1_,_000|MKP (Gain<br>_𝑛_=120|(%)), LLM:<br>_𝑛_=500|Gemma2-27b<br>_𝑛_=1_,_000|
|---|---|---|---|---|---|---|---|
|ACO+Random|ACO+LLM|0.00 ±0.00|-0.09±0.04|0.00±0.04|1.24±0.03|3.21±1.17|4.01±1.59|
|ACO+EoH (ICML’24)|ACO+LLM|0.14±0.12|0.16±0.35|0.38±0.53|1.61<br>±0.48|4.42±1.10|5.81±1.40|
|ACO+ReEvo (NeurIPS’24)|ACO+LLM|0.66<br>±0.50|1.49<br>±0.25|2.01±0.34|1.59±0.72|4.67±0.95|6.31<br>±0.38|
|ACO+Hercules-P (ours)|ACO+LLM|0.08±0.08|1.47±0.16|2.04<br>±0.16|1.44±0.38|4.73<br>±0.90|6.14±1.21|
|ACO+Hercules (ours)|ACO+LLM|**0.84**±0.14|**1.64**±0.17|**2.19**±0.20|**1.99**±0.50|**6.40**±0.97|**8.22**±1.17|



**Table 5: Performance comparison of different NCO solvers on TSP and CVRP** 

|Algorithm|Type|<br>_𝑛_=200|TSP (Gain (<br>_𝑛_=500|%))<br>_𝑛_=1_,_000|C<br>_𝑛_=200|VRP (Gain<br>_𝑛_=500|(%))<br>_𝑛_=1_,_000|
|---|---|---|---|---|---|---|---|
|POMO+Random|NCO+GPT-4o-mini|**3.05**|-18.90|-35.10|**3.07**|1.14|**2.86**|
|POMO+EoH (ICML’24)|NCO+GPT-4o-mini|2.19|1.42|1.47|0.48|-1.83|0.27|
|POMO+ReEvo (NeurIPS’24)|NCO+GPT-4o-mini|2.38|-5.24|-2.78|0.34|-14.20|-3.01|
|POMO+Hercules-P (ours)|NCO+GPT-4o-mini|-0.10|-4.81|-3.58|-0.57|-3.29|-0.57|
|POMO+Hercules (ours)|NCO+GPT-4o-mini|2.49|**6.62**|**16.43**|1.53|**1.22**|1.59|
|LEHD+Random|NCO+GPT-4o-mini|9.93|**8.83**|5.44|1.72|2.33|1.68|
|LEHD+EoH (ICML’24)|NCO+GPT-4o-mini|**10.67**|7.73|6.09|6.62|3.57|0.47|
|LEHD+ReEvo (NeurIPS’24)|NCO+GPT-4o-mini|6.94|-1.78|1.56|10.19|4.97|0.70|
|LEHD+Hercules-P (ours)|NCO+GPT-4o-mini|9.55|7.53|**6.89**|4.44|2.45|0.75|
|LEHD+Hercules (ours)|NCO+GPT-4o-mini|7.46|6.64|5.14|**14.37**|**7.90**|**2.33**|



underscores this issue. On the other hand, Hercules-P reduces the overall search time to 77% (23.6/30.6) of that required by Hercules. Although Hercules-P uses approximately 1.5 times more context tokens than Hercules and ReEvo, it does not significantly increase the cost of generation tokens, which are typically more expensive [30]. This makes Hercules-P ideal for environments with limited computing resources. Notably, Random utilizes only 0.2k context tokens, because of its simple prompts used for heuristic generation. However, this simplicity limits its ability to derive well-performing heuristics. 

## **4.2 Constructive Heuristics to Solve TSP** 

To assess the generalization capabilities of Hercules and Hercules-P across different HG tasks, we employ them in this subsection to derive constructive heuristics, which sequentially select unvisited nodes for solving real-world TSPLIB benchmarks [34]. The seed function is genetic programming hyper-heuristic [9]. As shown in Table 3, Hercules achieves the highest average gain of 4.87% across eighteen TSPLIB instances, followed by EoH with the average gain of 4.8%. In contrast, both Random and ReEvo perform poorly, yielding negative gains on average, i.e., failing to improve the performance of the seed function. 

## **4.3 Deriving Heuristic Measures for ACO to Solve BPP, MKP, OP, and TSP** 

In this subsection, we exploit Hercules and Hercules-P to derive heuristic measures for Ant Colony Optimization (ACO) applied to the Bin Packing Problem (BPP) and Multiple Knapsack Problem (MKP). The seed function is a conventional ACO algorithm [8]. We adopt Llama3.1-405b to solve BPP while adopting Gemma2-27b to solve MKP. This is because Llama3.1-405b fails to improve the seed function of MKP regardless of which LLM-based HG algorithm is executed. As shown in Table 4, Hercules outperforms the other algorithms across all COPs and LLMs, with particularly strong performance observed when solving the 1,000-scale MKP, achieving an 



<!-- Start of picture text -->
14 OP 17.0 TSP<br>16.0<br>12<br>15.0<br>10<br>14.0<br>Random 10.0 Random<br>864 EoHReEvo 5.0 EoHReEvo<br>2 Hercules-P Hercules-P<br>0 Hercules 0.0 Hercules<br>0 25 50 75 100 0 25 50 75 100<br>The number of fitness evaluations The number of fitness evaluations<br>(a) OP (b) TSP<br>Gain (%) Gain (%)<br><!-- End of picture text -->

**Figure 5: Convergence curves of different HG algorithms.** 

8.22% gain. In addition, when using Llama3.1-405b, Random fails to derive superior heuristics compared to the original ACO, while EoH achieves only a modest improvement, falling short when compared to the substantial gains obtained by Hercules-P and Hercules. In addition, Figure 5 presents the convergence curves of various LLMbased HG algorithms during their search processes for deriving ACO heuristic measures to solve the Orienteering Problem (OP) and TSP. The adopted LLM is GLM-4-Plus. As shown in Figure 5, Hercules and Hercules-P consistently derive better heuristics more efficiently than other LLM-based HG algorithms, during the entire search process. This is primarily attributed to the proposed CAP. 

## **4.4 Reshaping Attention Scores for NCO to Solve TSP and CVRP** 

Recently, Wang et al. [40] demonstrated that reshaping attention scores can enhance the generalization performance of NCO solvers trained on small-scale COPs for solving large-scale COPs. To assess the effectiveness of Hercules and Hercules-P on NCO solvers, following [53], we select DAR [40] as the seed function for TSP 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 

**Table 6: Search time comparison of different LLM-based HG algorithms on diverse HG tasks** 

||Task|Algorithm|Random|EoH<br>(ICML’24)|ReEvo<br>(NeurIPS|’24)|Hercules-P<br>(ours)|Hercules<br>(ours)||
|---|---|---|---|---|---|---|---|---|---|
||TSP-P|OMO|15.95|18.17|17.89||**11.50**|22.12||
|Time (m)|CVRP-|POMO|16.86|30.54|29.57||**9.51**|10.28||
||TSP-L|EHD|30.58|39.55|37.25||**28.72**|41.43||
||CVRP-|LEHD (_𝑛_=200)|45.73|67.27|61.58||**31.20**|42.80||
||CVRP-|LEHD (_𝑛_=500)|149.31|224.01|215.61||**110.28**|178.01||
||CVRP-|LEHD (_𝑛_=1_,_000)|639.83|854.25|854.71||**310.98**|757.67||
|Algorithm<br>G|**f**<br>ain (%)|**Table 7: Ablation s   f**<br>Algorithm|**tudy resul  f**<br>Gain (%)|**ts on differ**<br>Algorithm|**fent desi**<br>|**f gn cho**<br>Gain (%|**f  ices**<br>)<br>Algorit|hm|Gain (%)<br>GP|
|w/o CAP|3.12|Hercules (_𝜆_=0_._5)|5.96|w/o ConS||-4.06|Hercule|s-P (_𝛿_=0_._2)|T-4<br>7.01|
|w/o rank-based selection|8.49|Hercules (_𝜆_=0_._9)<br>Hercules (_𝜆_=1)|8.90<br>5.60|w/o EXEM|PLAR|-0.30|Hercule|s-P (_𝛿_=0_._3)|o-mini<br>6.21|
|Hercules (w/o PPP)|**11.10**|Hercules (_𝜆_=0_._7)|**11.10**|Hercules-|P|**7.46**|Hercule|s-P (_𝛿_=0_._1)|**7.46**|



and the vanilla POMO [18] and LEHD [27] as seed functions for Capacitated Vehicle Routing Problem (CVRP). As shown in Table 5, Random outperforms the other four LLM-based HG algorithms on certain tasks. A plausible reason for this is that the LLM corpora may lack sufficient knowledge of emerging NCO domains, thus limiting the performance of the other four LLM-based HG algorithms. Nevertheless, the heuristics derived by Hercules outperform the corresponding seed functions across a wider range of tasks compared to Random. For example, Hercules performs better than Random on the 500- and 1,000-node scales for the TSP-POMO task. In addition, in Table 6, we present the search time of different LLM-based HG algorithms across diverse NCO tasks. As shown in Table 6, Hercules-P outperforms the other LLM-based HG algorithms in terms of search time, while Random ranks at the second place. On these NCO tasks, Hercules-P reduce the search time by 48%, 7%, 31%, 27%, 38%, and 59%, respectively, when compared to Hercules. This reduction in search time is especially significant for large-scale COPs, where search can extend to several hours. In such cases, incorporating PPP demonstrates high efficiency in reducing resource expenditure. 

## **4.5 Ablation Studies** 

In this subsection, we conduct ablation studies to investigate the effectiveness of the design choices of Hercules and Hercules-P, and present the results in Table 7. The adopted HG task is deriving penalty heuristics for GLS to solve TSPs (see Section 4.1). Specifically, w/o CAP refers to the setting using RP to provide search directions, w/o rank-based selection refers to the setting that randomly selects parent heuristics, w/o ConS refers to the setting that PPP assumes all predictions are accurate, and w/o EXEMPLAR refers to the setting that heuristic examples are randomly selected from the current population. For all the other experiments presented in this paper, _𝜆_ = 0 _._ 7 is applied for Hercules, and _𝛿_ = 0 _._ 1 is applied for Hercules-P. As shown in Table 7, when CAP is omitted, the gain decreases by 7.98%, further demonstrating that CAP produces more specific search directions. In addition, the proposed rank-based selection mechanism significantly contributes to the superior performance of Hercules. For Hercules-P, ConS effectively determines unreliable predictions, preventing them from negatively affecting the derivation of high-performance heuristics. Finally, when EXEMPLAR is omitted, the gain decreases by 7.76%, mainly due to the 

associated degradation in predictive accuracy (elaborated in the following paragraph). 

We further present the predictive accuracy 1.0 of PPP with and withw/ EXEMPLAR w/ EXEMPLAR-U out EXEMPLAR, both 0.8 w/o EXEMPLAR of which are executed ten times, aiming to per0.6 form meaningful statistical tests. In addition, we 0.4 include w/ EXEMPLARU as an additional setting, 0.2 where w/ EXEMPLAR-U is able to select heuris0.0 tics with identical fitness **Figure 6: Ablation study on dif-** values. To assess whether **ferent EXEMPLAR variants.** different versions of EX- 

EMPLAR can accurately predict the fitness values of the produced heuristics, we need to set a quantifying measure. Specifically, we intuitively deem a prediction accurate if the absolute error between the predicted fitness value and the true fitness value is less than _𝛿_ · ( _𝑢𝑏𝑡_ − _𝑙𝑏𝑡_ ). As shown in Figure 6, the inclusion of EXEMPLAR improves the median of predictive accuracy by 26% and 37% (both significantly different: _𝑝_ =0.048 and 0.004) when compared to w/ EXEMPLAR-U and w/o EXEMPLAR, respectively. In addition, the Pearson correlation coefficient analysis reveals a correlation coefficient of 0.39, indicating a moderate linear relationship between the predicted and true values. The one-way ANOVA test results yield a _𝑝_ -value of 0.6, suggesting that the mean difference between the predicted and true values is not statistically significant. It is imperative to clarify that although the proposed PPP may seem less accurate in predicting heuristic performance, the values shown in Figure 6 are determined by a strict measure of fitness values as aforedefined and they do not exhibit a strong correlation with the overall performance of Hercules-P, because many produced heuristics are reevaluated (see ConS in Section 3.2). As discussed in Sections 4.1 and 4.4, Hercules-P reduces search time by 7%∼59% when compared to Hercules, while achieving on-par gain. We strongly believe that PPP is highly beneficial for HG tasks that require rapid solutions, e.g., deriving heuristics for the dynamic, near-real-time allocation 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models 

of resources in 5G mobile edge cloud networks [19]. We plan to extend PPP by integrating it with other methods, such as beam search, to further enhance its predictive accuracy. 

## **5 Conclusion** 

To derive well-performing heuristics, we propose Hercules, which exploits our proprietary CAP to abstract the core components from elite heuristics, to produce more specific search directions. In addition, we introduce Hercules-P, a resource-efficient variant that integrates CAP with our novel PPP. PPP exploits previously evaluated heuristics to predict the performance of newly produced ones, thereby reducing the required computing resources for heuristic evaluations. The experimental results demonstrate the effectiveness of Hercules, Hercules-P, and all our designed mechanisms. 

## **Acknowledgments** 

This work was supported in part by the Jilin Provincial Department of Science and Technology Project under Grant 20230201083GX. We also thank the Computing Center of Jilin Province for providing technical support. 

## **References** 

- [1] Florian Arnold and Kenneth Sörensen. 2019. Knowledge-guided local search for the vehicle routing problem. _Computers & Operations Research_ 105 (2019), 32–46. 

- [2] Bowen Baker, Otkrist Gupta, Nikhil Naik, and Ramesh Raskar. 2017. Designing neural network architectures using reinforcement learning. In _the International Conference on Learning Representations_ . 1–18. 

- [3] Yoshua Bengio, Andrea Lodi, and Antoine Prouvost. 2021. Machine learning for combinatorial optimization: A methodological tour d’horizon. _European Journal of Operational Research_ 290, 2 (2021), 405–421. 

- [4] Aigerim Bogyrbayeva, Meraryslan Meraliyev, Taukekhan Mustakhov, and Bissenbay Dauletbayev. 2024. Machine learning to solve vehicle routing problems: A survey. _IEEE Transactions on Intelligent Transportation Systems_ 25, 6 (2024), 4754–4772. 

- [5] Edmund K Burke, Michel Gendreau, Matthew Hyde, Graham Kendall, Gabriela Ochoa, Ender Özcan, and Rong Qu. 2013. Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ 64, 12 (2013), 1695–1724. 

- [6] Lin Chen, Fengli Xu, Nian Li, Zhenyu Han, Meng Wang, Yong Li, and Pan Hui. 2024. Large language model-driven meta-structure discovery in heterogeneous information network. In _Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 307–318. 

- [7] Xiangxiang Chu, Shun Lu, Xudong Li, and Bo Zhang. 2023. MixPath: A unified approach for one-shot neural architecture search. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 5972–5981. 

- [8] Marco Dorigo, Mauro Birattari, and Thomas Stutzle. 2006. Ant colony optimization. _IEEE Computational Intelligence Magazine_ 1, 4 (2006), 28–39. 

- [9] Gabriel Duflo, Emmanuel Kieffer, Matthias R Brust, Grégoire Danoy, and Pascal Bouvry. 2019. A GP hyper-heuristic approach for generating TSP heuristics. In _Proceedings of IEEE International Parallel and Distributed Processing Symposium Workshops_ . 521–529. 

- [10] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. 2023. Retrieval-augmented generation for large language models: A survey. arXiv: 2312.10997. 

- [11] Keld Helsgaun. 2017. _An extension of the Lin-Kernighan-Helsgaun TSP solver for constrained traveling salesman and vehicle routing problems: Technical report_ . 

- [12] Qingchun Hou, Jingwei Yang, Yiqiang Su, Xiaoqing Wang, and Yuming Deng. 2023. Generalize learned heuristics to solve large-scale vehicle routing problems in real-time. In _the International Conference on Learning Representations_ . 1–37. 

- [13] Zhiyuan Hu, Chumin Liu, Xidong Feng, Yilun Zhao, See-Kiong Ng, Anh Tuan Luu, Junxian He, Pang Wei Koh, and Bryan Hooi. 2024. Uncertainty of thoughts: Uncertainty-aware planning enhances information seeking in large language models. In _the International Conference on Learning Representations Workshop on Large Language Model (LLM) Agents_ . 

- [14] Zhehui Huang, Guangyao Shi, and Gaurav S. Sukhatme. 2024. Can large language models solve robot routing? arXiv: 2403.10795. 

- [15] Ganesh Jawahar, Muhammad Abdul-Mageed, Laks V. S. Lakshmanan, and Dujian Ding. 2024. LLM performance predictors are good initializers for architecture search. In _the Findings of the Association for Computational Linguistics_ . 10540– 10560. 

- [16] Zhuoxuan Jiang, Haoyuan Peng, Shanshan Feng, Fan Li, and Dongsheng Li. 2024. LLMs can find mathematical reasoning mistakes by pedagogical chain-of-thought. 

In _Proceedings of the International Joint Conference on Artificial Intelligence_ . 3439– 3447. 

- [17] R. E. Keller and R. Poli. 2007. Linear genetic programming of parsimonious metaheuristics. In _Proceedings of the IEEE Congress on Evolutionary Computation_ . 4508–4515. 

- [18] Yeong-Dae Kwon, Jinho Choo, Byoungjip Kim, Iljoo Yoon, Youngjune Gwon, and Seungjai Min. 2020. POMO: Policy optimization with multiple optima for reinforcement learning. In _Proceedings of the Advances in Neural Information Processing Systems_ . 21188–21198. 

- [19] Nadia Motalib Laboni, Sadia Jahangir Safa, Selina Sharmin, Md. Abdur Razzaque, Md. Mustafizur Rahman, and Mohammad Mehedi Hassan. 2024. A hyper heuristic algorithm for efficient resource allocation in 5G mobile edge clouds. _IEEE Transactions on Mobile Computing_ 23, 1 (2024), 29–41. 

- [20] Liam Li and Ameet Talwalkar. 2020. Random search and reproducibility for neural architecture search. In _Proceedings of Uncertainty in Artificial Intelligence_ . 367–377. 

- [21] Fei Liu, Xi Lin, Zhenkun Wang, Qingfu Zhang, Tong Xialiang, and Mingxuan Yuan. 2024. Multi-Task learning for routing problem with cross-problem zeroshot generalization. In _Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 1898–1908. 

- [22] Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Proceedings of the International Conference on Machine Learning_ . 32201–32223. 

- [23] Fei Liu, Xialiang Tong, Mingxuan Yuan, and Qingfu Zhang. 2023. Algorithm evolution using large language model. arXiv: 2311.15249. 

- [24] Jingyu Liu, Jun Ai, Minyan Lu, Jie Wang, and Haoxiang Shi. 2023. Semantic feature learning for software defect prediction from source code and external knowledge. _Journal of Systems and Software_ 204 (2023), 111753. 

- [25] Tennison Liu, Nicolás Astorga, Nabeel Seedat, and Mihaela van der Schaar. 2024. Large language models to enhance bayesian optimization. In _the International Conference on Learning Representations_ . 1–33. 

- [26] Yuqiao Liu, Yehui Tang, Zeqiong Lv, Yunhe Wang, and Yanan Sun. 2022. Bridge the gap between architecture spaces via a cross-domain predictor. In _Proceedings of the Advances in Neural Information Processing Systems_ . 13355–13366. 

- [27] Fu Luo, Xin Li, Fei Liu, Qingfu Zhang, and Zhenkun Wang. 2023. Neural combinatorial optimization with heavy decoder: Toward large scale generalization. In _Proceedings of the Advances in Neural Information Processing Systems_ . 8845–8864. 

- [28] Qitan Lv, Jie Wang, Hanzhu Chen, Bin Li, Yongdong Zhang, and Feng Wu. 2024. Coarse-to-fine highlighting: Reducing knowledge hallucination in large language models. In _Proceedings of the International Conference on Machine Learning_ . 32612– 32642. 

- [29] Zeyuan Ma, Hongshu Guo, Jiacheng Chen, Guojun Peng, Zhiguang Cao, Yining Ma, and Yue-Jiao Gong. 2024. LLaMoCo: Instruction tuning of large language models for optimization code generation. arXiv: 2403.01131. 

- [30] OpenAI. [n. d.]. https://openai.com/api/pricing/. 

- [31] M. Padberg and G. Rinaldi. 1987. Optimization of a 532-city symmetric traveling salesman problem by branch and cut. _Operations Research Letters_ 6, 1 (1987), 1–7. 

- [32] Zhengzhong Qiu, Wei Bi, Dong Xu, Hua Guo, Hongwei Ge, Yanchun Liang, Heow Pueh Lee, and Chunguo Wu. 2023. Efficient self-learning evolutionary neural architecture search. _Applied Soft Computing_ 146 (2023), 110671. 

- [33] César Rego, Dorabela Gamboa, Fred Glover, and Colin Osterman. 2011. Traveling salesman problem heuristics: Leading methods, implementations and latest advances. _European Journal of Operational Research_ 211, 3 (2011), 427–441. 

- [34] Gerhard Reinelt. 1991. TSPLIB—A traveling salesman problem library. _ORSA journal on computing_ 3 (1991), 376–384. 

- [35] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. 2024. Mathematical discoveries from program search with large language models. _Nature_ 625 (2024), 468–475. 

- [36] Zhiqing Sun and Yiming Yang. 2023. DIFUSCO: Graph-based diffusion solvers for combinatorial optimization. In _Proceedings of the Advances in Neural Information Processing Systems_ . 3706–3731. 

- [37] Niki van Stein and Thomas Bäck. 2024. LLaMEA: A large language model evolutionary algorithm for automatically generating metaheuristics. 

- [38] Mark P. Wachowiak, Mitchell C. Timson, and David J. DuVal. 2017. Adaptive particle swarm optimization with heterogeneous multicore parallelism and GPU acceleration. _IEEE Transactions on Parallel and Distributed Systems_ 28, 10 (2017), 2784–2793. 

- [39] Mingzhao Wang, You Zhou, Zhiguang Cao, Yubin Xiao, Xuan Wu, Wei Pang, Yuan Jiang, Hui Yang, Peng Zhao, and Yuanshu Li. 2025. An Efficient Diffusion-based Non-Autoregressive Solver for Traveling Salesman Problem. In _Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 1469–1480. 

- [40] Yang Wang, Ya-Hui Jia, Wei-Neng Chen, and Yi Mei. 2024. Distance-aware attention reshaping: Enhance generalization of neural solver for large-scale vehicle routing problems. arXiv: 2401.06979. 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 

- [41] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. 2022. Chain-of-thought prompting elicits reasoning in large language models. In _Proceedings of the Advances in Neural Information Processing Systems_ . 24824–24837. 

- [42] Junru Wu, Xiyang Dai, Dongdong Chen, Yinpeng Chen, Mengchen Liu, Ye Yu, Zhangyang Wang, Zicheng Liu, Mei Chen, and Lu Yuan. 2021. Stronger NAS with weaker predictors. In _Proceedings of the Advances in Neural Information Processing Systems_ . 28904–28918. 

- [43] Xuan Wu, Jizong Han, Di Wang, Pengyue Gao, Quanlong Cui, Liang Chen, Yanchun Liang, Han Huang, Heow Pueh Lee, Chunyan Miao, You Zhou, and Chunguo Wu. 2023. Incorporating Surprisingly Popular Algorithm and Euclidean distance-based adaptive topology into PSO. _Swarm and Evolutionary Computation_ 76 (2023), 101222. 

- [44] Xuan Wu, Di Wang, Huanhuan Chen, Lele Yan, Yubin Xiao, Chunyan Miao, Hongwei Ge, Dong Xu, Yanchun Liang, Kangping Wang, Chunguo Wu, and You Zhou. 2024. Neural Architecture Search for Text Classification with Limited Computing Resources Using Efficient Cartesian Genetic Programming. _IEEE Transactions on Evolutionary Computation_ 28, 3 (2024), 638–652. 

- [45] Xuan Wu, Di Wang, Lijie Wen, Yubin Xiao, Chunguo Wu, Yuesong Wu, Chaoyu Yu, Douglas L. Maskell, and You Zhou. 2024. Neural combinatorial optimization algorithms for solving vehicle routing problems: A comprehensive survey with perspectives. arXiv: 2406.00415. 

- [46] Xingyu Wu, Sheng-hao Wu, Jibin Wu, Liang Feng, and Kay Chen Tan. 2025. Evolutionary computation in the era of large language model: Survey and roadmap. _IEEE Transactions on Evolutionary Computation_ 29, 2 (2025), 534–554. 

- [47] Yaoxin Wu, Wen Song, Zhiguang Cao, Jie Zhang, and Andrew Lim. 2022. Learning improvement heuristics for solving routing problems. _IEEE Transactions on Neural Networks and Learning Systems_ 33, 9 (2022), 5057–5069. 

- [48] Yubin Xiao, Di Wang, Boyang Li, Mingzhao Wang, Xuan Wu, Changliang Zhou, and You Zhou. 2024. Distilling Autoregressive Models to Obtain HighPerformance Non-Autoregressive Solvers for Vehicle Routing Problems with Faster Inference Speed. In _Proceedings of the AAAI Conference on Artificial Intelligence_ . 20274–20283. 

- [49] Yubin Xiao, Di Wang, Xuan Wu, Yuesong Wu, Boyang Li, Wei Du, Liupu Wang, and You Zhou. 2025. Improving generalization of neural vehicle routing problem solvers through the lens of model architecture. _Neural Networks_ 187 (2025), 107380. 

- [50] Yixing Xu, Yunhe Wang, Kai Han, Yehui Tang, Shangling Jui, Chunjing Xu, and Chang Xu. 2021. ReNAS: Relativistic evaluation of neural architecture search. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 4411–4420. 

- [51] Bing Xue, Mengjie Zhang, Will N. Browne, and Xin Yao. 2016. A survey on evolutionary computation approaches to feature selection. _IEEE Transactions on Evolutionary Computation_ 20, 4 (2016), 606–626. 

- [52] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V Le, Denny Zhou, and Xinyun Chen. 2024. Large language models as optimizers. In _the International Conference on Learning Representations_ . 1–42. 

- [53] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Parkand, and Guojie Song. 2024. Large language models as hyperheuristics for combinatorial optimization. In _Proceedings of the Advances in Neural Information Processing Systems_ . 

- [54] Chris Ying, Aaron Klein, Eric Christiansen, Esteban Real, Kevin Murphy, and Frank Hutter. 2019. NAS-Bench-101: Towards reproducible neural architecture search. In _Proceedings of the International Conference on Machine Learning_ . 7105– 7114. 

- [55] Junchi Yu, Ran He, and Zhitao Ying. 2024. Thought Propagation: An analogical approach to complex reasoning with large language model. In _the International Conference on Learning Representations_ . 1–27. 

- [56] Zhi-Hui Zhan, Jun Zhang, Yun Li, and Henry Shu-Hung Chung. 2009. Adaptive particle swarm optimization. _IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)_ 39, 6 (2009), 1362–1381. 

- [57] Fangfang Zhang, Yi Mei, Su Nguyen, and Mengjie Zhang. 2021. Correlation coefficient-based recombinative guidance for genetic programming hyperheuristics in dynamic flexible job shop scheduling. _IEEE Transactions on Evolutionary Computation_ 25, 3 (2021), 552–566. 

- [58] Huaixiu Steven Zheng, Swaroop Mishra, Xinyun Chen, Heng-Tze Cheng, Ed H. Chi, Quoc V Le, and Denny Zhou. 2024. Take a step back: Evoking reasoning via abstraction in large language models. In _the International Conference on Learning Representations_ . 1–38. 

- [59] Jianan Zhou, Yaoxin Wu, Wen Song, Zhiguang Cao, and Jie Zhang. 2023. Towards omni-generalizable neural methods for vehicle routing problems. In _Proceedings of the International Conference on Machine Learning_ . 42769–42789. 

## **A Derivation of Information Gain Formula** 

Proposition 1. _The information gain from abstracting core components is equal to:_ 





_𝐼𝐺_ (Ω _𝑡_ ) = _𝐻_ (Ω _𝑡_ ) − _𝑝_ 0 _𝐻_ (Ω0) −· · · − _𝑝𝑘𝐻_ (Ω _𝑘_ ) 



According to the conditional probability, _𝑝 𝑗_ · _𝑝_ ( _𝜔𝑖_ |Ω _𝑗_ ) = _𝑝_ ( _𝜔𝑖_ |Ω _𝑡_ ), ∀ _𝑗_ ∈{0 _,_ 1 _,_ · · · _,𝑘_ }. Thus, the _𝑗_ th term simplifies to the following expression: 



Therefore, we conclude that 

_𝐼𝐺_ (Ω _𝑡_ ) = − <u>∑</u> _𝑘_ ︁ _𝑗_ =0<sup>_𝑝𝑗_log</sup><sup>_𝑝𝑗._</sup> (9) When ∀ _𝑗_ ∈{0 _,_ 1 _,_ · · · _,𝑘_ } _, 𝑝 𝑗_ = _𝑘_ +11<sup>,</sup><sup>_𝐼𝐺_(Ω</sup><sup>_𝑡_)reaches its maximum</sup> value of log( _𝑘_ + 1). When ∃ _𝑗_ ∈{0 _,_ 1 _,_ · · · _,𝑘_ } s.t. _𝑝 𝑗_ = 1, _𝐼𝐺_ (Ω _𝑡_ ) reaches its minimum value of 0. However, due to the diverse nature of LLM training corpora, the LLM will not consistently provide the same direction. Therefore, by abstracting core components, the unspecificity (entropy) can decrease within the (0 _,_ log( _𝑘_ + 1)] interval. □ 

It is important to note that each heuristic may consist of multiple core components, or the same core component may be used across multiple heuristics. However, to simplify the deduction procedures, we assume a one-to-one correspondence between core components and heuristics in our analysis. This assumption does not affect the validity of our conclusion that _𝐼𝐺_ (Ω _𝑡_ ) = −<sup>�</sup><sup>_𝑘_</sup> _𝑗_ =0<sup>_𝑝𝑗_log</sup><sup>_𝑝𝑗_, whose</sup> value ranges within the (0 _,_ log( _𝑘_ + 1)] interval, because the made assumption primarily serves to streamline the proof process. Specifically, if the number of core components _𝑘𝑐_ differs from the number of heuristics _𝑘_ , _𝐼𝐺_ (Ω _𝑡_ ) would be partitioned into _𝑘𝑐_ + 1 subsets instead of _𝑘_ + 1 (the assumed case of a one-to-one correspondence between core components and heuristics). Despite this difference, the mathematical framework for entropy and information gain remains unchanged except the said replacement of _𝑘_ with _𝑘𝑐_ . In addition, our framework is designed in a way that a single core component can map to multiple search directions, rather than having a single search direction corresponding to multiple core components. For example, the core component “Normalizing values” may correspond to directions such as “Normalize penalties relative to 

Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

**Table 8: Parameters of Hercules and Hercules-P** 

|Parameter|Value|
|---|---|
|LLM temperature|1|
|CAP coefficients_𝑘, 𝜆_|5, 0.7|
|Maximum number of evaluations|100|
|Population size_𝑁_, Crossover rate, Mutation rate|15, 1, 0.5|
|ConS coefficients_𝛿, 𝛼, 𝛽_|0.1, 0.5, 0.8|



overall distance” or “Normalize distances effectively to balance contributions”. This assumption ensures flexibility in mapping core components to directions. Therefore, we deem our assumption of partitioning all possible directions into mutually exclusive subsets associated with core components is reasonable. 

## **B Adopted Crossover, Elitist Mutation Operators, and Other EC Definitions** 

For Hercules and Hercules-P, each heuristic code snippet denotes an individual within the population. Parent heuristics refer to the heuristics selected according to Eq. (5), which are utilized during the crossover and mutation processes to derive offspring heuristics. Elite heuristics denote the top- _𝑘_ heuristics selected based on corresponding fitness values within the current population. During population initialization, we employ a simple prompt proposed by [53] to guide the LLM in randomly deriving the initial population. For consistency, we adopt the crossover and mutation operators proposed by [53] in all the experiments presented in this paper. Specifically, for the adopted crossover operator, two distinct parent heuristics are selected according to Eq. (5). Subsequently, the relative fitness values of these two heuristics determine which one serves as the primary learning exemplar for deriving an offspring heuristic. The employed mutation operator is elitist mutation, which derives multiple heuristics based on the historically best heuristic, aiming to produce high-performance ones. 

## **C Detailed Hyper-parameters and Experimental Setups** 

**_Hardware_** We comprehensively evaluate the performance of all algorithms, using a computer equipped with an Intel(R) Xeon(R) W-2235 CPU. 

**_Hyper-parameters._** In Table 8, we present the hyper-parameters of Hercules and Hercules-P. In addition, following the prior study [53], the temperature of the LLM is increased by 0.3 during the initial phase to enhance the diversity of the initial population. For the parameters of seed functions (e.g., KGLS parameters), we adopt the configurations specified in the prior study [53] to ensure a fair comparison. This study also documents the definitions of all HG tasks used in this paper. In addition, following the prior study [53], the performance metric for TSP and CVRP is the gap, which is defined as the relative difference in the “average length” between corresponding heuristics and LKH3 [11]. For BPP and MKP, the performance metrics are the number of bins used and the total profit, respectively. For OP, the performance metric is the total prize collected by visiting nodes. 

Finally, for all experiments in this paper, we exploit the training and test datasets to derive heuristics and assess the final derived heuristics, respectively. Specifically, during the search process, the performance of heuristics on the training datasets determines their 

**Table 9: Performance comparison of different GLS algorithms on a real-world TSP instance** 

|Algorithm|Gain (%)|Length (mile)|
|---|---|---|
|KGLS-Random|0.24|10836.79|
|KGLS-EoH (ICML’24)|0.38|10821.49|
|KGLS-ReEvo (NeurIPS’24)|0.29|10831.75|
|KGLS-Hercules-P (ours)|0.17|10842.03|
|KGLS-Hercules (ours)|**2.07**|**10637.36**|



**Table 10: Performance comparison of different LLM-based HG algorithms on TSP_LEHD task** 

|Algorithm|<br>_𝑛_=200|TSP (Gain (<br>_𝑛_=500|%))<br>_𝑛_=1_,_000|GL|
|---|---|---|---|---|
|LEHD+Random|8.48|8.36|7.70|M-|
|LEHD+EoH (ICML’24)|10.84|9.47|8.06|4-0|
|LEHD+ReEvo (NeurIPS’24)|10.13|8.70|6.97|520|
|LEHD+Hercules-p (ours)|9.98|8.80|**11.72**||
|LEHD+Hercules (ours)|**11.06**|**9.24**|8.16||



fitness values. The heuristic with the best performance on the training dataset is selected as the final derived heuristic. We then further assess the performance of all final derived heuristics on test datasets and report the average experimental results in Section 4. The details of training datasets and test datasets of all HG tasks can be found in the prior study [53]. 

## **D Prompts Used in Hercules and Hercules-P** 

Prompts used for Hercules or Hercules-P can be categorized as problem-specific prompts (e.g., the heuristic description, COP description, seed function, and function signature) and general prompts (e.g., prompts for CAP and PPP). All these prompts are available in the provided source code link. 

## **E Additional Experimental Results** 

## **E.1 Real-world Case Study** 

To better illustrate the improved efficiency by adopting Hercules to derive heuristics in real-world scenarios, we examine a widely used real-world demonstration task of visiting all state capital cities in the United State (excluding Alaska and Hawaii) as a case study [31]. In this task, each capital city is treated as a node, framing the problem as a 49-node TSP instance. In addition, in this section, we directly compare the KGLS algorithms derived from different LLM-based HG methods in Section 4.1. As shown in Table 9, the Hercules-derived algorithms reduce the total mileage by nearly 200 miles compared to other algorithms, demonstrating the significant practical advantages of Hercules. 

## **E.2 Additional Experiments of Reshaping** 

## **Attention Scores for NCO** 

In this subsection, we adopt GLM-4-0520 as the LLM to further assess the performance of Hercules in reshaping attention scores for LEHD to solve large-scale TSP instances. In the experiments conducted in this subsection, we derive heuristics using training sets of problem sizes 200, 500, and 1,000 and evaluate their performance on test sets of the corresponding sizes. As shown in Table 10, Hercules achieves the best performance on test datasets with 200 and 500 nodes, while Hercules-P outperforms on the 1,000-node scale, achieving a gain of 11.72% over the seed function. 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Xuan Wu et al. 

**Table 11: Performance comparison of different ACO algorithms on CVRP under black-box and white-box settings** 

|Algorithm|LLM|Gain (%<br>Black-box|),_𝑛_= 50<br>White-box|
|---|---|---|---|
|ACO+Random|GLM-4-Plus|29.60|47.65|
|ACO+EoH (ICML’24)|GLM-4-Plus|41.33|48.43|
|ACO+ReEvo (NeurIPS’24)|GLM-4-Plus|34.35|45.48|
|ACO+Hercules-p (ours)|GLM-4-Plus|38.50|47.49|
|ACO+Hercules (ours)|GLM-4-Plus|**41.70**|**48.92**|
|ACO+Hercules (ours)|Qwen2.5-14B|-|44.99|



## **E.3 Performance of Different ACO Algorithms on CVRP under Black-box Settings** 

Following the setup in the prior study [53], we assess the performance of different HG methods under black-box conditions, where no information about the COPs is provided to the LLM. We adopt GLM-4-Plus as the LLM and task it with deriving heuristic measures for ACO to solve CVRP. The experimental results demonstrate that Hercules outperforms the other HG methods. In addition, it is worth noting that Hercules performs well even when using a small-scale LLM (Qwen2.5-14B, distilled from DeepSeek-R1). 

## **F Search Directions Produced by RP and CAP** 

In this section, we present additional search directions produced by RP [53] and CAP (our method) across various HG tasks, COPs, and LLMs. Additionally, all produced unspecific search directions are highlighted in blue. For example, GPT-4o-mini frequently suggests the term “edge clustering", when performing RP. This direction "edge clustering" is frequently applied in tasks like recommender systems, where it helps identify patterns in user interactions and preferences. However, it is not commonly used in heuristic algorithms for solving COPs and is, therefore, considered unspecific. 

### **Direction 1: The produced search directions for deriving penalty heuristics to solve TSP** 

<mark># The LLM used to provide search directions is GPT -4o-mini.</mark> **<mark>RP</mark>** <mark>:</mark> 

<mark>Consider</mark> **<mark>edge_clustering</mark>** <mark>, incorporate</mark> **<mark>historical_edge_frequencies</mark>** <mark>, and adapt penalties dynamically based on current path exploration.</mark> **<mark>CAP</mark>** <mark>: Focus on relative edge scoring , incorporate multiple factors like connectivity and distance , and enhance normalization techniques. # The LLM used to provide search directions is Llama -3-70b.</mark> **<mark>RP</mark>** <mark>: Normalize and</mark> **<mark>symmetrize</mark>** <mark>heuristics; consider</mark> **<mark>the_opposite</mark>** <mark>(not including an edge) for more effective penalties.</mark> 

**<mark>CAP</mark>** <mark>: Focus on relative edge costs (e.g., proximity concept) rather than absolute deviations from average distance.</mark> 

### **Direction 3: The produced search directions for reshaping attention scores of POMO to solve CVRP** 

<mark># The LLM used to provide search directions is GPT -4o-mini.</mark> **<mark>RP</mark>** <mark>: Incorporate</mark> **<mark>route_clustering</mark>** <mark>, demand distribution analysis , and consider multi -vehicle interactions for enhanced heuristics.</mark> **<mark>CAP</mark>** <mark>: Emphasize vectorization over loops for performance. Enhance demand penalties to better reflect capacity constraints. Normalize distances effectively to balance contributions.</mark> 

### **Direction 4: The produced search directions for reshaping attention scores of LEHD to solve TSP** 

<mark># The LLM used to provide search directions is GPT -4o-mini.</mark> **<mark>RP</mark>** <mark>: Incorporate</mark> **<mark>edge_connectivity</mark>** <mark>to prioritize clusters. Consider spatial locality using coordinates for refinement. Adaptively adjust weights based on</mark> **<mark>current_solution_state</mark>** <mark>.</mark> **<mark>CAP</mark>** <mark>: Use logarithmic scaling for distances , increase top -K selection , and implement normalization for better convergence and stability.</mark> 

## **G Heuristics Derived by EoH and Hercules** 

In this section, we present the final derived heuristics for solving BPP derived by EoH and Hercules, repsectively. It is evident that, when Llama3.1-405b is adopted, EoH fails to derive intricate heuristics, which accounts for its poor performance in solving BPP (see Table 4). 

**EoH 1: The ACO heuristic measure produced by EOH using Llama3.1-405b for solving BPP.** 

**def** EoH_1(demand: **np** . **ndarray** , capacity: **int** ) -> **np** . **ndarray** : demand_ratio = demand / capacity 

- **return np** .tile( **np** . **power** (demand_ratio, 2), (demand. **shape** [0], 1)) * (1 - demand_ratio[:, **np** . newaxis]) 

However, despite using the same LLM, Hercules is able to generate more intricate heuristics, one of which is presented as follows: 

**Heuristic 1: The ACO heuristic measure produced by Hercules using Llama3.1-405b for solving BPP.** 

**def heuristic** (demand: **np** . **ndarray** , capacity: **int** ) -> **np** . **ndarray** : 

This function calculates the heuristics for the Bin Packing Problem (BPP). Parameters: 

demand (np.ndarray): A 1D array representing the sizes of the items. capacity (int): The capacity of each bin. 

Returns: 

np.ndarray: A 2D array where heuristics[i][j] represents how promising it is to put item i and item j in the same bin. 

- # Calculate the complementarity of each pair of items 

- # The complementarity is the difference between the capacity and the sum of the demands of the two items 

complementarity = capacity - **np** . **add** . **outer** (demand, demand) 

- # Apply exponential decay to the complementarity values 

- # This reduces the dominance of large values and emphasizes the importance of small values decayed_complementarity = **np** . **exp** (-complementarity / capacity) 

- # Normalize the demand values to be between 0 and 1 

### **Direction 2: The produced search directions for deriving ACO heuristic measures to solve BPP** 

<mark># The LLM used to provide search directions is Llama3 .1-405b.</mark> **<mark>RP</mark>** <mark>: Consider non -linear relationships between demand ratios and heuristics , and</mark> **<mark>experiment</mark>** <mark>with different sparsification thresholds for better performance.</mark> **<mark>CAP</mark>** <mark>:</mark> 

normalized_demand = demand / demand. **max** () 

- # Calculate the heuristic value for each pair of items 

- # The heuristic value is the product of the normalized demands and the decayed complementarity 

heuristics = **np** . **outer** (normalized_demand, normalized_demand) * decayed_complementarity 

# Sparsify the matrix by setting unpromising elements to zero 

# Here, we consider elements with a value less than 0.5 as unpromising 

heuristics[heuristics < 0.5] = 0 

**return** heuristics 

<mark>Simplification and normalization of demand values can lead to more effective heuristics , reducing computational complexity.</mark> 

