# **HeurAgenix: Leveraging LLMs for Solving Complex Combinatorial Optimization Challenges** 

**Xianliang Yang**<sup>1</sup> **Ling Zhang**<sup>1</sup> **Haolong Qian**<sup>1</sup><sup>_,_2</sup> **Lei Song**<sup>1</sup> **Jiang Bian**<sup>1</sup> 

1Microsoft Research Asia, Beijing, China 

2Tsinghua University, Beijing, China 

```
{Xianliang.Yang,Ling.Zhang,v-haolqian,Lei.Song,Jiang.Bian}
```

```
@microsoft.com
```

## **Abstract** 

Heuristic algorithms play a vital role in solving combinatorial optimization (CO) problems, yet traditional designs depend heavily on manual expertise and struggle to generalize across diverse instances. We introduce **HeurAgenix** , a two-stage hyper-heuristic framework powered by large language models (LLMs) that first evolves heuristics and then selects among them automatically. In the heuristic evolution phase, HeurAgenix leverages an LLM to compare seed heuristic solutions with higher-quality solutions and extract reusable evolution strategies. During problem solving, it dynamically picks the most promising heuristic for each problem state, guided by the LLM’s perception ability. For flexibility, this selector can be either a state-of-the-art LLM or a fine-tuned lightweight model with lower inference cost. To mitigate the scarcity of reliable supervision caused by CO complexity, we fine-tune the lightweight heuristic selector with a dual-reward mechanism that jointly exploits singals from selection preferences and state perception, enabling robust selection under noisy annotations. Extensive experiments on canonical benchmarks show that HeurAgenix not only outperforms existing LLM-based hyper-heuristics but also matches or exceeds specialized solvers. Code is available at `https://github.com/microsoft/HeurAgenix` . 

## **1 Introduction** 

Combinatorial optimization (CO) problems are fundamental in operations research and critical for decision-making across various industries [14, 40]. These problems often involve large-scale search spaces, where dimensionality grows exponentially, making traditional solution methods computationally intractable [42, 2]. This complexity has led to the widespread use of heuristics, which provide approximate solutions within a feasible time frame [44, 48]. Heuristics are typically designed to be interpretable, with clear rule-based decision-making processes that enhance transparency and human understanding. 

Despite their effectiveness, heuristics heavily rely on manual expertise and are challenging to adapt to changing conditions. In response, hyper-heuristics have emerged, aiming to automate heuristic design by crafting rules for their selection and combination [8, 9]. Although hyper-heuristics offer interpretability, they often require manual rule design, which limits adaptability to evolving problem states [43, 5]. 

Recent advancements in large language models (LLMs) have inspired work on automatic heuristic design, using LLMs to generate and refine heuristics through few-shot prompting and code synthesis [47, 36, 63, 41]. Although these approaches attain strong performance on moderate-sized classic CO problems, most of them embed the LLM-produced heuristic inside a task-specific solver, 

This is the notice string that will appear at the bottom of the first page. 



Figure 1: Overview of the HeurAgenix framework for automatic heuristic design and adaptive selection. In the heuristic evolution phase, an LLM autonomously discovers evolution strategies by analyzing contrastive solution tuples, while in the problem solving phase, an adaptive heuristic selection mechanism integrates Test-time Scaling (TTS) [59, 58]. 

which resulting reliance on hand-crafted domain knowledge constrains heuristic flexibility and the generalization. 

To address these limitations, we introduce **HeurAgenix** , a unified framework for automatic heuristic evolution and adaptive selection. To the best of our knowledge, HeurAgenix is the first LLM-based hyper-heuristic framework that simultaneously (i) evolves a diverse pool of heuristics without relying on any external solver and (ii) incorporates an online heuristic selector for adaptive problem solving. Depending on user requirements, the second phase can leverage either an frontier LLM (such as GPT [1], DeepSeek [18]) or a fine-tuned lightweight model for efficient inference. A diagram illustrating the proposed framework is provided in Figure 1. A diagram illustrating the proposed framework is provided in Figure 1. Our main contributions are: 

- We introduce **HeurAgenix** , a versatile framework for automatic heuristic evolution and selection. It offers scalable and generalizable solutions for complex CO problems, outperforming existing hyper-heuristic approaches. 

- We propose a **contrastive, data-driven heuristic evolution** phase, analyzing solution trajectories to discover evolution strategies without predefined rules. We develop an **adaptive heuristic selection mechanism** that integrates LLM and TTS, which selects heuristics based on the current problem state and improve efficiency and solution quality. 

2 

- To train the heuristic selector more robustly under noisy data, we introduce a **dual-reward mechanism** that combines context perception for accurate state recognition with outcome preference that amplifies the positive/negative margin. 

## **2 Preliminary and Related Work** 

In this section, we present the important definitions and notations employed throughout this paper. 

### **2.1 Heuristics for CO Problems** 

**Problem state** In CO problems, directly characterizing a problem instance and its solution can be challenging, as they are often represented in complex numerical data structures. To address this, following the CO community, we adopt the concept of a **problem state** as an abstract representation capturing the high-level features of both the problem instance and its current (partial) solution [10]. For example, in the Traveling Salesman Problem (TSP), static problem states may include features such as the number of nodes, average inter-node distance, and graph symmetry, while dynamic problem states can describe aspects such as visited nodes and current tour cost. 

**Heuristic** In this paper, we define a heuristic algorithm as a function that maps a **problem state** _z_ to an **operation** _O_ . Formally, a heuristic _H_ can be described as _H_ : _Z →O_ , where _Z_ represents the space of problem states and _O_ is the set of allowable operations. If the heuristic is a **constructive heuristic** , the operation _O_ may involve adding elements to extend a partial solution. Conversely, if the heuristic is an **improvement heuristic** , _O_ might involve exchanging, replacing, or perturbing existing elements to refine the solution [24]. Detailed designs for heuristics, problem states and operations are provided in the Appendix E. 

**Transition function.** For a problem instance _d_ we first define the single-step **transition function** 

_T_ : _Z × O −→Z,_ 

which deterministically maps the current state and an applied operation to the next state. For later convenience we extend the definition of _T_ to accept a heuristic as its second argument: 



that is, query the heuristic for its chosen operation at _z_ and then perform the original state update. Repeatedly executing the same heuristic _H_ for exactly _M_ steps is denoted 



a shorthand we will use extensively in Section 3.2 when defining the selector’s optimization target. 

**Solution trajectory.** Given a sequence of heuristics ( _H_ 0 _, . . . , Hn−_ 1), the resulting trajectory is _z_ 0 = Init( _d_ ) _, O_ 0 = _H_ 0( _z_ 0) _, z_ 1 = _T_ ( _z_ 0 _, O_ 0) _, . . . , On−_ 1 = _Hn−_ 1( _zn−_ 1) _, zn_ = _T_ ( _zn−_ 1 _, On−_ 1) _,_ where _zi_ is the state before step _i_ and _Oi_ the selected operation. We write the trajectory as _S_ = _{_ ( _zi, Oi_ ) _}_<sup>_n_</sup> _i_ =0<sup>_−_1and denote its objective cost by</sup><sup>_C_(</sup><sup>_S_).</sup> 

**Heuristic selector.** Given the problem state _z ∈Z_ , the remaining decisions _t ∈{_ 0 _, . . . , T }_ , and the heuristic pool _H_ , we define a heuristic selector as a mapping 



which selects the heuristic _π_ ( _z, t_ ) at problem state _z_ when _t_ decisions remain. 

### **2.2 Hyper-Heuristics** 

In the CO community, hyper-heuristics have been introduced to manipulate heuristics. Two main categories are generation hyper-heuristics and selection hyper-heuristics [10]. 

3 

**Generation hyper-heuristics** involve the automatic creation of heuristics by systematically combining elementary operations or decision-making rules. These techniques often employ methods such as genetic programming, genetic algorithms, and particle swarm optimization [28, 51]. Although these methods can yield high-performing algorithms, they often encounter challenges related to computational overhead and adaptability [61, 31]. 

**Selection hyper-heuristics** dynamically choose the most appropriate heuristic from a predefined set by evaluating the current problem state. These methods incorporate rule-based, meta-heuristic, or learning-based strategies, rendering them effective for complex optimization tasks. Nevertheless, they may struggle with intricate selection mechanisms and generalization issues [20, 16, 17, 52]. 

### **2.3 LLMs for Combinatorial Optimization** 

Table 1: Comparison of LLM-based CO paradigms. 

|Paradigm|Heuristic Evolution|Problem Solving|Solver Required<sup>_∗_</sup>|
|---|---|---|---|
|FunSearch|LLM-driven|Fixed heuristic|Yes|
|EoH|5 manually designed strategies|Fixed heuristic|Yes|
|ReEvo|Feedback-based refinement|Fixed heuristic|Yes|
|AlphaEvolve|Ensemble LLM-driven evolution|Fixed heuristic|No|
|HeurAgenix (Ours)|Contrastive, data-driven evolution|Adaptive selection|No|



> _∗_ A solver refers to either: a traditional optimization solver (e.g., GLS [57]), a neural network-based solver (e.g., PoMo [34]), or a specialized hyper-heuristic algorithm (e.g., ACO [19]). 

LLMs have demonstrated significant potential in addressing combinatorial optimization (CO) problems. For instance, Zhang et al. [64] assessed the performance of LLMs on various graph optimization challenges, while Iklassov et al. [30] developed effective prompting strategies to enable LLMs to adapt to diverse problem formulations. Xiao et al. [62] introduced the Chain-of-Experts approach, integrating multi-agent cooperation to directly address optimization tasks. These studies underscore LLMs’ flexibility and capability in reasoning within CO problems. 

Particularly relevant to our work are studies focusing on LLMs for heuristic generation and evolution in CO problem solving. FunSearch [47] employs LLMs to iteratively generate and refine candidate solutions, aiming to improve solution quality. EoH [36] facilitates multi-directional evolution to boost heuristic diversity, while ReEvo [63] leverages LLM-driven reflection for targeted optimization. Collectively, these efforts highlight LLMs’ potential in automating heuristic design and enhancing optimization processes. Most recently, AlphaEvolve [41] pushes the paradigm further by pairing an ensemble of Gemini [54] LLMs with automated evaluators in an evolutionary loop, enabling the discovery of entire algorithmic codebases that optimise practical systems. 

However, as illustrated in Table 1, methods such as FunSearch, EoH, and ReEvo couple the LLMgenerated heuristic with a task-specific solver, which limits generalization and demands domain expertise. AlphaEvolve removes the external solver by evolving complete programs, yet its offline evolutionary loop is computationally intensive and does not provide instance-level adaptation at inference time. In contrast, HeurAgenix supports flexible real-time heuristic selection by leveraging either an LLM or a fine-tuned lightweight model. This enables autonomous data-driven evolution and on-the-fly adaptation among multiple heuristics without dependency on external solvers, thus forming a truly end-to-end optimization paradigm. 

### **2.4 Test-time Scaling** 

Test-time scaling (TTS) is the practice of intentionally spending extra computation at inference time to improve answer quality [26, 23, 55]. Early research demonstrated a compute–accuracy trade-off in progressive or interruptible inference; recent LLM work has turned TTS into a standard tool for eliciting stronger reasoning, for example by sampling multiple candidate outputs and selecting the best one with a lightweight verifier [59, 58]. Representative instantiations include Best-of- _N_ sampling [6] and Diverse-Verifier Tree Search (DVTS) [12]. Our framework adopts the same searchverifier philosophy in problem solving phase to trade a modest increase in inference compute for substantial gains in solution quality and robustness. 

4 

### **2.5 Challenges in Noisy Data for Long-Term Decision-Making** 

Training models for effective long-term decision making is fundamentally challenged by the difficulty of accurately assessing the true long-term value of each action (i.e., selecting a particular heuristic at a given step). This difficulty stems from the credit-assignment problem: the ultimate impact of a single selection may only emerge after many steps or even after the whole trajectory, which complicates isolating its precise contribution, especially within large state–action spaces and over extended horizons. Exhaustively evaluating the long-term utility of early selections would require enumerating every possible continuation, which is computationally infeasible [60]. 

As a result, any practical evaluation procedure can provide only approximate, noisy scores based on a small subset of rollouts. Training models on such imperfect feedback therefore demands robust learning techniques. HeurAgenix meets this need via a dual-reward mechanism that fuses final-solution preferences with intermediate-reasoning signals, yielding more reliable supervision for heuristic selection under noisy annotations. 

## **3 Methodology** 

HeurAgenix is designed to leverage the complementary strengths of generation and selection hyperheuristics, offering a robust framework for combinatorial optimization. 

As illustrated in Figure 1, the generative component utilizes the reasoning abilities of LLMs to autonomously refine and evolve heuristic algorithms across diverse problem instances. Meanwhile, the selection component enhances adaptability by dynamically choosing the most suitable heuristic based on the current problem state, employing a fine-tuned lightweight model. By unifying these methods, HeurAgenix achieves high performance and adaptability, effectively addressing the challenges of large-scale CO problems. 

### **3.1 Heuristic Evolution** 

Heuristic evolution is a systematic, data-driven procedure that iteratively improves a **seed heuristic** _H_ seed. We leverage an LLM both to diagnose structural weaknesses and to propose concrete evolution strategies that amend them. 

Let _D_ evo and _D_ val denote the evolution and validation instance sets, respectively. Building on the definitions in Section 2.1, a single evolution round proceeds as follows: 

**Step 1: Basic solution generation.** For every _d ∈D_ evo we run _H_ seed to obtain a **basic solution** _S_ = _{_ ( _zi, Oi_ ) _}_<sup>_n_</sup> _i_ =0<sup>_−_1and its cost</sup><sup>_C_(</sup><sup>_S_).If</sup><sup>_H_seedis a constructive heuristic, it is applied repeatedly</sup> from the initial state until a feasible complete solution is constructed. If _H_ seed is an improvement heuristic, we first sample a constructive heuristic _Hc_ to obtain an initial feasible solution, then apply _H_ seed iteratively as a local search or improvement operator. 

**Step 2: Contrastive solution generation.** To reveal potential weaknesses, we perform up to _P_ perturbation trials. In each trial we (i) randomly select a subset _K ⊂{_ 0 _, . . . , n −_ 1 _}_ of operation indices in the basic solution, (ii) replace every _Ok_ ( _k ∈K_ ) by an alternative _Ok_<sup>_′∈O_(</sup><sup>_zk_)</sup><sup>_\ {Ok}_,</sup> (iii) roll out the modified trajectory to obtain a perturbed solution _S_<sup>_′_</sup> and its cost _C_ ( _S_<sup>_′_</sup> ). Whenever _C_ ( _S_<sup>_′_</sup> ) _< C_ ( _S_ ) (for minimization problems), _S_<sup>_′_</sup> is stored as a **contrastive solution** ; its mutation list _M_ = _{_ ( _zk, Ok, Ok_<sup>_′_)</sup><sup>_}k∈K_becomes a candidate operation set for evolution.</sup> 

**Step 3: Critical operation identification.** Not all modified operations in _M_ are responsible for the performance gap, so we first identify the decisive mutation. For each ( _zk, Ok, Ok_<sup>_′_)</sup><sup>_∈M_we</sup> independently replace _Ok_ with _Ok_<sup>_′_, keep all other operations still from</sup><sup>_Hseed_, and if the solution are</sup> valid, measure the individual improvement 



where _S_<sup>(</sup><sup>_k_)</sup> is the solution obtained after changing only the _k_ -th operation (positive ∆ _k_ denotes improvement for a minimization task). We then select _k_<sup>_⋆_</sup> = arg max _k∈K_ ∆ _k_ and _Ok⋆_ is the **critical operation** . 

5 

**Step 4: Extract evolution strategy.** The tuple ( _zk⋆ , Ok⋆ , Ok_<sup>_′⋆_) and the current heuristic</sup><sup>_H_seedare</sup> passed to the LLM: 

_E_ = LLMevolve� _H_ seed _, zk⋆ , Ok⋆ , Ok_<sup>_′⋆_</sup> � _._ 

The LLM explains why _Ok_<sup>_′⋆_is better and outputs an</sup><sup>**evolution strategy**</sup><sup>_E_.This strategy serves as a</sup> conceptual guide to improve _H_ seed, potentially involving modifications such as parameter adjustment, the addition of control logic, or component replacement. 

**Step 5: Iterative refinement.** Starting from _H_ 0 = _H_ seed, we refine the heuristic for at most _T_ max = rounds. After each round we compute the performance _pi_ = evaluate_performance� _Hi, D_ val� _|D_ <u>1val</u> _|_ � _d∈D_ val<sup>_C_</sup> � _Sd_<sup>_i_</sup> �, where _Sd_<sup>_i_denotesthesolutionproducedby</sup><sup>_Hi_oninstance</sup><sup>_d_,andobtain</sup> an update _Hi_ +1 = LLMrefine� _Hi, E, pi_ � _._ We stop early if no further improvement is observed. Algorithm 1 summarizes the entire procedure. Figure 2 also visualizes how a single critical operation mutation is extracted and justified. 

**Algorithm 1** One Round Heuristic Evolution 

**Input:** seed heuristic _H_ seed; evolution instance _d_ ; validation set _D_ val; LLM; maximum perturbation trials _P_ ; maximum refinement trials _I_ max 

**Output:** refined heuristic _H_ evolved 

1: # Step 1: Basic Solution Generation 2: _S ←_ run_heuristic( _H_ seed _, d_ ) _▷S_ = _{_ ( _zi, Oi_ ) _}_<sup>_n_</sup> _i_ =0<sup>_−_1</sup> 

3: _n ←|S|_ 

4: # Step 2: Contrastive Solution Generation 5: _M ←_ ∅; _p ←_ 0 6: **while** ( _p < P_ ) _∧_ ( _M_ = ∅) **do** 7: _p ← p_ + 1 8: _K ←_ sample_indices( _n_ ) _▷_ a random subset of operation indices 9: _S_<sup>_′_</sup> _←_ perturb( _S, K_ ) _▷_ replace each _Ok_ with _Ok_<sup>_′_</sup> 10: **if** _C_ ( _S_<sup>_′_</sup> ) _< C_ ( _S_ ) **then** _▷_ for a minimization problem 11: _M ←{_ ( _zk, Ok, Ok_<sup>_′_)</sup><sup>_}k∈K_</sup> 12: **end if** 

13: **end while** 

14: **if** _M_ = ∅ **then** 15: **return** _H_ seed _▷_ no better contrastive solution found 

16: **end if** 

17: # Step 3: Critical Operation Identification 18: **for all** ( _zk, Ok, Ok_<sup>_′_)</sup><sup>_∈M_</sup><sup>**do**</sup> 19: _S_<sup>(</sup><sup>_k_)</sup> _←_ perturb_single( _S, k, Ok_<sup>_′_)</sup> 20: ∆ _k ← C_ ( _S_ ) _− C_ ( _S_<sup>(</sup><sup>_k_)</sup> ) 21: **end for** 22: _k_<sup>_⋆_</sup> _←_ arg max _k_ ∆ _k_ 23: ( _zk_<sup>_⋆_</sup> _, Ok_<sup>_⋆_</sup> _, Ok_<sup>_′⋆_)</sup><sup>_←_tuple with index</sup><sup>_k⋆_</sup> 

24: # Step 4: Extract Evolution Strategy 25: _E ←_ LLMevolve( _H_ seed _, zk_<sup>_⋆_</sup> _, Ok_<sup>_⋆_</sup> _, Ok_<sup>_′⋆_)</sup> 

26: # Step 5: Iterative Heuristic Refinement 

27: _t ←_ 0; _H_ 0 _← H_ seed; _improved ←_ **true** 

28: **while** _improved ∧ i < I_ max **do** 

29: _pi ←_ evaluate_performance( _Hi, D_ val) 

30: _Hi_ +1 _←_ LLMrefine( _Hi, E, pi_ ) 31: _pi_ +1 _←_ evaluate_performance( _Hi_ +1 _, D_ val) 

- 32: **if** _pi_ +1 _< pi_ **then** 

- for a minimization problem 

33: _i ← i_ + 1 

34: **else** 

- 35: _improved ←_ **false** 

- 36: **end if** 

37: **end while** 

38: _H_ evolved _← Hi_ 39: **return** _H_ evolved 

6 



Figure 2: Illustration of one heuristic-evolution step on a four-node TSP evolution instance. The cumulative effect of this and subsequent refinements can be seen in Figure 3. 



Figure 3: Example of heuristic evolution for TSP. The left panel illustrates successive strategy refinements and their impact on TSPLIB [46] performance. The right panel details a specific evolution step, where an alternative cost function is induced by the LLM based on counterfactual analysis. For a step-by-step extraction of the refinement highlighted in Round 2, see Figure 2 and for further details and code, see Appendix C. 

**Algorithmic Summary and Discussion.** Each round of evolution enhances the heuristic in a datadriven manner. By repeating the process over diverse evolution instances and aggregating the learned strategies, the heuristic pool _H_ grows in diversity and effectiveness. Figure 3 gives an overview of multiple rounds of evolution and their corresponding performance changes. For further details on an evolution example and hyper-parameter choices, refer to Appendix C and Appendix E. 

### **3.2 Problem Solving** 

**Motivation.** Even after evolution, a single heuristic rarely dominates across all problem states; performance varies sharply with the current state. Static, hand-crafted switching rules therefore lack adaptability [11, 27, 33]. We therefore require a real-time selector that decides which heuristic should be applied next for each encountered state _z_ (defined as Section 2.1). 

**Heuristic selection objective.** Following the notation of Section 2.1, for a minimization problem we jointly define the state-value function, the action value of a heuristic, and the corresponding 

7 

heuristic selector: 



### where 

- _N_ is the maximum number of heuristic calls, 

- _M_ is the fixed number of consecutive steps per chosen heuristic, 

- _t_ represents remaining decisions (where _t_ = 0 means termination), 

- _Sz_ is the current solution corresponding to state _z_ , and 

- _H_ denotes the evolved heuristic pool. 

From these, _V_ ( _z, t_ ) represents the expected cost from state _z_ with _t_ decisions remaining, _Q_ ( _z, H, t_ ) evaluates a heuristic’s performance in that state, and _π_<sup>_⋆_</sup> ( _z, t_ ) represents the optimal selector that chooses heuristics with minimum _Q_ . The objective of heuristic selector optimization is to determine the optimal selector. For simplicity, we will omit the parameter _t_ if it is clear from the context. 

**Heuristic selection procedure.** In practice, obtaining _Q_ ( _z, H_ ) exactly is infeasible. Monte-Carlo simulation is a common surrogate, but exhaustively simulating every heuristic in _H_ is prohibitively slow on large instances, whereas an LLM—relying on coarse semantic cues alone—typically misses the best choice. We therefore adopt a hybrid strategy: the LLM first prunes the pool to a compact candidate set, after which a lightweight test-time search (TTS) evaluates those candidates and selects the one to execute: 

**Step 1: Filter candidate heuristics.** The LLM filters the heuristic pool to produce a candidate subset _H_<sup>_′_</sup> = LLMfilter( _z, H_ ). 

**Step 2:** by Monte-Carlo search [ **Evaluate value of heuristics.** 53]: _Q_ ˆ _H_ = mcFor every_evaluate( _Hz, H∈H_ )<sup>_′_</sup> . Specifically, we first apply itunder problem state _z_ , we estimate its value _H_ sequentially _M_ times starting from state _z_ , resulting in a new intermediate state. From the intermediate state, we then generate _T_ candidate solutions by repeatedly selecting heuristics randomly from _H_ until completion. The estimated value _Q_<sup>ˆ</sup> _H_ is the average terminal cost over the _T_ rollouts—averaging provides an unbiased estimate of the expected outcome, while taking a minimum would introduce a downward bias and favor lucky samples. Implementation details appear in Appendix D. 

**Step 3: Select the most suitable heuristic.** Select _H_<sup>ˆ</sup> = arg min _H∈H′ Q_<sup>ˆ</sup> _H_ and execute it _M_ times. This structured approach couples rapid LLM-based reasoning with a lightweight search verifier, yielding a balanced and efficient solver that leverages both model guidance and TTS. 

**Problem solving process.** Based on this heuristic selector, we can dynamic select the heuristic and solve problem easily. For a test instance _d_ we proceed iteratively. Starting from the initial state _z_ , the selector chooses a heuristic _H_<sup>ˆ</sup> , and then execute _H_<sup>ˆ</sup> is executed _M_ times, to update the problem . The cycle repeats until none of the available heuristics can further improve the solution. The hyper-parameter _M_ balances decision frequency against runtime overhead and is set to _M_ = 5 throughout all experiments. 

### **3.3 Selection Model Fine-tuning** 

**Motivation** Selecting the optimal heuristic in real-time plays a crucial role in combinatorial optimization performance. To enhance efficiency, we propose the implementation of lightweight selection models within HeurAgenix to effectively manage latency, computational demands, and resource utilization. This approach is particularly beneficial as it allows for multiple heuristic evaluations and selections without incurring prohibitive inference costs associated with larger models. 

8 

Lightweight models face inherent limitations in processing complex problem states and applying various heuristics effectively, particularly in their ability to adaptively select appropriate heuristics for different scenarios. To address these challenges, we propose a fine-tuning approach that enhances the model’s comprehension of both the problem domain and available heuristics. Our methodology begins with an offline data collection process, followed by a detailed analysis of our implementation strategy for extracting insights from non-optimal and noisy datasets. 

**Offline Data Collection** We construct an offline dataset consisting of tuples ( _z, H, QH_ ). Here _z_ is the current problem state, _H_ is the candidate heuristic drawn from the pool _H_ , and _QH_ is the rollout value assigned to _H_ at state _z_ . To obtain _QH_ , every heuristic in _H_ is evaluated from the initial state _z_ by the Monte Carlo pipeline of selection, expansion, simulation, and back-propagation (see Appendix D), yielding a scalar score for that ( _z, H_ ) pair. 

To obtain data that is both informative and robust, we collect two types of trajectories. (i) Greedy trajectories update the state with the heuristic that attains the highest _QH_ at each step, exposing the selector to near-optimal decisions. (ii) Stochastic trajectories update the state with a random heuristic, forcing the selector to recover from non-optimal contexts. The resulting mixture encourages the model to associate diverse states with effective heuristics. 

As noted in Section 2.5, the rollout values _QH_ are inherently noisy because only a small subset of future continuations can be explored. We therefore employ the dual-reward fine-tuning scheme to learn policies that remain reliable under such imperfect supervisory signals. 

**Dual-Reward Design** To mitigate the impact of noisy evaluation scores, we equip the selector with a dual-reward mechanism that restructures supervision signals instead of propagating raw values. As shown in Figure 4, the mechanism combines a Preference-based Outcome Reward (POR) and a Context-Perception Reward (CPR); two lightweight auxiliary rewards enforce output format and language consistency similar as in [50]. 



Figure 4: Detailed reward design, showing the operational mechanisms of the novel POR and CPR as well as auxiliary Format Reward [50] and Language Rewards [18]. 

**Preference-based Outcome Reward (POR)** Following the analysis in Section 2.5, the rollout values produced by the MCTS evaluator are inevitably noisy: similar heuristics may receive widely different scores across runs, while heuristics with genuinely different performance can end up with almost identical scores. Such distortions mislead the learner and weaken the training signal. 

Figure 5 shows that, for our selection tasks, choosing any heuristic from a small positive set is nearly as good as always picking the single best one, whereas selecting from the complementary negative set quickly harms solution quality. In practice, mild noise is sufficient to interchange the ranks of neighbouring heuristics, yet it rarely pushes a truly positive heuristic into the negative set (or vice-versa) because the gap between the two sets is usually large. 

These observations motivate a reward design that compresses score differences within the positive or negative group while enlarging the margin between the two groups. Let the rollout scores _{QH }H∈H_ be sorted in descending order for the current state _z_ . Suppose the model proposes a heuristic _H_<sup>ˆ</sup> 

9 



Figure 5: Effect of noisy rollout data on heuristic selection ( `rd100` in TSPLIB [46]). Y-axis: expected optimality gap (lower is better) after completing the tour by random sampling. X-axis: decision rounds. Blue: always selecting the best heuristic (oracle). Green: uniformly selecting from the top 30% heuristics (positive set). Red: random selection. Selecting from the positive set almost matches the oracle and clearly outperforms random choice. 

ranked at position _ℓ_ . Two thresholds _n_ pos _< n_ neg _≤ n_ = _|H|_ divide the list into a positive region, a negative region, and an error region. The preference-based outcome reward is then defined as 



Linear interpolation reduces gaps inside each region, whereas the coefficients _Rp_ and _Rn_ amplify the discontinuity at the region boundary; heuristics in the error region receive a fixed penalty _−RL_ . Consequently, POR is insensitive to small permutations inside the positive set but still yields a strong gradient whenever a heuristic crosses the positive/negative border. 

The robustness of POR is demonstrated with a four-heuristic toy example (Table 2). Heuristics are divided into a positive set (top two ranks) and a negative set (bottom two). We compare POR ( _Rp_ = _Rn_ = 1) with the Normalized Rank Reward (NRR), a common RLHF baseline that linearly maps ranks to [ _−_ 1 _,_ 1] [65, 13]. Under noise free scores, both rewards differentiate the two sets. When two middle scores are noised, NRR almost eliminates the gap between H2 and H3 (0 _._ 2 vs _−_ 0 _._ 2), while POR still keeps a clear margin (0 _._ 5 vs _−_ 0 _._ 5). Hence POR supplies a much steadier learning signal in the presence of measurement noise. 

Table 2: Toy example comparing POR with Normalized Rank Reward (NRR). NRR maps ranks to [ _−_ 1 _<u>,</u>_ 1]. “Noisy” columns show the effect after perturbing the two middle scores. 

|Heuristic|Actual score|Actual NRR|Actual POR|Noisy score|Noisy NRR|Noisy POR|
|---|---|---|---|---|---|---|
|H1|1.0|1.0|1.0|1.0|1.0|1.0|
|H2|0.8|0.6|0.5|0.6|0.2|0.5|
|H3|0.2|-0.6|-0.5|0.4|-0.2|-0.5|
|H4|0.0|-1.0|-1.0|0.0|-1.0|-1.0|



**Context-Perception Reward (CPR)** CPR explicitly rewards the selector for understanding the environment, rather than for matching a potentially noisy scalar outcome. Recent evidence shows 

10 

that even when the final reward signal is noisy or even random, models can still improve provided that their reasoning traces remain correct and receive feedback [49]. Moreover, empirical studies demonstrate that an accurate internal perception of the task state is often a stronger predictor of downstream performance than the magnitude of the terminal reward itself [32]. Motivated by these findings, CPR encourages the model to align its latent representation with the ground-truth state. 

Formally, let _z_ = ( _z_ 1 _, . . . , zm_ ) be the true feature vector of the current problem state and _z_ ˆ = (ˆ _z_ 1 _, . . . ,_ ˆ _zm_ ) the selector’s own prediction of these _m_ features, we get: 



where I( _·_ ) is the indicator function and _Ri_<sup>+</sup><sup>_>_0(</sup><sup>_R_</sup> _i_<sup>_−>_0)denotesthepositive(negative)reward</sup> tied to the _i_ -th feature. Correctly perceived dimensions therefore yield positive feedback, while misperceptions are penalized, pushing the selector toward a faithful contextual understanding before it commits to a heuristic decision. Figure 6 visualizes how CPR rectifies qualitative judgment errors and guides the model toward more accurate state assessments. 



Figure 6: Impact of the CPR mechanism in rectifying qualitative judgment errors during LLM inference. The illustration shows how CPR guides the model toward accurate contextual assessments, mitigating errors that might otherwise remain uncorrected. 

**Training Procedure** Under the dual-reward design, the selection model’s parameters _θ_ are finetuned offline using the Group Relative Policy Optimization (GRPO) [50] method. GRPO’s key approach involves leveraging inter-response preference relations to iteratively update the policy parameters _θ_ . This framework aims to optimize the likelihood that the model generates response sequences leading to higher cumulative evaluation scores _R_ total. The goal of this training process is to enable the selection model to proficiently generate heuristic sequences that yield superior performance scores, thus improving its effectiveness in real-world applications of combinatorial optimization. The Algorithm 2 outlines the training process. 

## **4 Experiments** 

In this section, we conduct a comprehensive evaluation of HeurAgenix under diverse settings to assess its performance, robustness, and adaptability. We explore heuristic evolution outcomes in Section 4.1, analyze problem solving efficiency using LLMs in Section 4.2, and investigate the capabilities of fine-tuned models in Section 4.3. To ensure fairness and consistency throughout our experiments, we adhere to the following setup and more detailed parameter settings can be found in Appendix E: 

1. **Foundation Model:** In the heuristic evolution phase, GPT-4o (version: 2024-11-20) is employed as the foundation model for heuristic evolution and problem solving phase. To ensure fair comparisons, we consistently use this model across all LLM-based hyperheuristics, including EoH and ReEvo. In the problem solving phase using LLMs, GPT-4o continues as the primary selector, while Qwen-7B [3] serves as the base model for fine-tuning in the fine-tuned model experiments. 

11 

|**Algor**|**ithm 2**Fine-tuningPipeline for Heuristic Selection|
|---|---|
|**Input**l<br>(_G, M_|offline dataset_D_offline; initial policy_πθ_0; reward weights_λ_POR_, λ_CPR _(optional λbase)_; hyper-parameters<br>epochs_, B_size_, ϵ, β, µ_)|
|1: _π_<br>|_θ ←πθ_0<br>_▷_Base selector policy<br>|
|2: **fo**|**r**epoch_e_= 1**to**_M_epochs **do**<br>|
|3:<br>|Sample mini-batch_{zk}_<sup>_B_size</sup><br>_k_=1 <sup>_⊂D_offline</sup><br>|
|4:|**for**each state_zk_ **do**<br><br><br>|
|5:|Sample_G_heuristic sequences<br>�<br>_H_<sup>(</sup><sup>_g_)</sup><br>_k_<br>�_G_<br>_g_=1 <sup>_∼πθ_(</sup><sup>_· | zk_)</sup>|
|6:|**for**_g_ = 1**to**_G_**do**<br>|
|7:|Compute_R_POR(_zk, H_<sup>(</sup><sup>_g_)</sup><br>_k_ <sup>)</sup><br>_▷_Refer equation (2)<br>|
|8:|Compute_R_CPR(_zk_)<br>_▷_Refer equation (3)<br>|
|9:|Compute_R_base(_zk, H_<sup>(</sup><sup>_g_)</sup><br>_k_ <sup>)</sup><br>_▷_Following the GRPO methodology<br>|
|10:<br>11:|_R_<sup>(</sup><sup>_g_)</sup><br>_k_<br>_←λ_POR_R_POR+_λ_CPR_R_CPR+_λ_base_R_base<br>**end for**<br><sup>�</sup><br><br><br><br><sup>_′_</sup>|
|12:|Estimate group-relative advantages <br>_A_<sup>(</sup><sup>_g_)</sup><br>_k_<br>= _R_<sup>(</sup><sup>_g_)</sup><br>_k_<br>_−_<sup>1</sup><br>_G_<br>�<br>_g_<sup>_′ R_(</sup><sup>_g_)</sup><br>_k_<br>for all_g_.<br>_▷_GRPO core<br>|
|13:|**for**inner step_u_= 1**to**_µ_**do**|
|14:<br>15:<br>|Update_πθ_ by maximizing GRPO objective with clip_ϵ_and KL penalty_β_<br>**end for**<br>|
|16:|**end for**|
|17: **e**|**nd for**|
|**Outp**|**ut**fine-tunedparameters_θ_|



2. **API Calls:** During heuristic evolution, all hyper-heuristics evolve until they reach 2,000 API calls, ensuring consistency across methods. In problem solving, our method utilizes _⌈ M_<sup>_<u>N</u>⌉_+ 2 API calls—where</sup><sup>_N_is max heuristic steps and related to problem size and</sup><sup>_M_is</sup> fixed at 5, with 2 additional calls for problem description and heurisitic pool introduction. 

3. **Execution Time:** Each test instance is allocated a maximum runtime of two hours to exploit the advantages of search-based methods. 

4. **Metric:** Solution performance is quantified by the optimality-gap metric, gap =<sup>_<u>v−</u>_</sup> _v_<sup>_uvu_</sup> _×_ 100%, where _v_ is the obtained solution value and _v_<sup>_u_</sup> is the known optimal (or best-known) value. To reduce variance, every experiment is run three times. 

5. **Platform:** Experiments are conducted on a GNU/Linux system with a 5.15.0-121-generic kernel, Intel(R) Xeon(R) processor, NVIDIA RTX A6000 (48G) GPU, and CUDA 12.2. 

We evaluate our framework across the following combinatorial optimization problems: 

1. **Traveling Salesman Problem (TSP):** Utilizes sub-datasets from TSPLIB [46] to identify the shortest route visiting each city once. 

2. **Capacitated Vehicle Routing Problem (CVRP):** Employs the largest instances from the first six series of CVRPLIB [45] to optimize delivery routes with capacity constraints. 

3. **Multiple Knapsack Problem (MKP):** Uses instances from mknapcb1 and mknapcb4 in the OR-Library [4] to maximize item value across multiple knapsacks. 

4. **Job Shop Scheduling Problem (JSSP):** Leverages the first 20 instances from the ORLibrary [4] to minimize total processing time for jobs across machines. 

5. **MaxCut Problem (MaxCut):** Uses the first 10 instances from Optsicom [15] to partition graph vertices and maximize the edge weight sum between vertex sets. 

### **4.1 Evolution Experiments** 

In this section, we evaluate the effectiveness of our heuristic evolution strategy on five combinatorial optimization problems. Since the evolution interfaces of ReEvo and EoH are limited to the nearest neighbor heuristic in TSP, we compare with these two baselines only in that setting; for all other problems, we contrast the original seed heuristics with the evolved variants produced by HeurAgenix. 

12 



Figure 7: Average optimality gaps (%; lower is better) before and after heuristic evolution on five representative CO problems. Complete results for all instances appear in Appendix F.1. 

As figure 7 the shows, HeurAgenix consistently and substantially reduces the gap, and even very basic seed heuristics can be transformed into highly competitive solvers through our automatic evolution pipeline. Detailed evolution results are provided in Table 5 in Appendix F.1. 

### **4.2 Problem Solving with LLM** 

We benchmark HeurAgenix on five standard CO benchmarks, always using GPT-4o as the heuristic selector for the evolved heuristic pool, and contrast its performance with both traditional methods and the strongest available LLM-based hyper-heuristics. 

For TSP we compare against Guided Local Search (GLS) [57], Ant Colony Optimization (ACO) [19], and OR-Tools [25], as well as three language-based hyper-heuristics: EoH [36]+GLS and ReEvo [63]+GLS, which keep the GLS framework but let EoH or ReEvo evolve its penalty function, and ReEvo+ACO, which uses ReEvo to refine the pheromone update rules of ACO. For CVRP we report ACO, OR-Tools, and ReEvo+ACO. For MKP we include ACO, ReEvo+ACO, the quantuminspired algorithm QICSA [35], and Particle Swarm Optimization (PSO) [21], with the QICSA and PSO numbers copied from Huang et al. [29]. The JSSP baselines are ACO, PSO, and the Grey Wolf Optimizer (GWO) [38] as reported by van Hoorn et al. [56]. The MaxCut baselines are Scatter Search (SS) [37], CirCut [7], and VNSPR [22], which are taken from Myklebust et al. [39]. 

As shown in Figure 8, HeurAgenix decisively outperforms the existing language-based hyperheuristics and matches or surpasses the specialized methods. Detailed performance results are provided in Table 6 in Appendix F.2. 

13 



Figure 8: Average optimality gap (%; lower is better) of HeurAgenix and baselines on five CO benchmarks. Dark-blue bars correspond to HeurAgenix (Ours), draw-orange bars to EoH related method, light-orange bars to ReEvo related methods, and gray bars to traditional methods. A dagger (†) after a method name indicates that the result is copied from the original publication. Complete results for all instances appear in Appendix F.2. 

### **4.3 Problem Solving with a Fine-tuned Model** 

We next investigate whether a lightweight model, fine-tuned under our dual-reward scheme, can serve as an effective online selector. All experiments are conducted on TSPLIB instances, where the selector must choose from the identical evolved heuristic pool. 

Table 3: Per-instance optimality gaps on TSPLIB (%; lower is better) when the selector is a mainstream LLM. **Bold** marks the best result. Variance is omitted when it equals 0. 

|Instance|GPT-4o|OpenAI O3|DeepSeek-R1|Ours|
|---|---|---|---|---|
|kroA100|**0**|**0**|**0**|**0**|
|kroA150|**0**|**0**|**0**|**0**|
|kroB100|**0**|**0**|**0**|**0**|
|kroB200|0.11|0.10_±_0.1|**0**|0.30_±_0.1|
|kroC100|**0**|**0**|**0**|**0**|
|bier127|1.29_±_0.6|**0.22**_±_0.1|1.01_±_0.1|1.09_±_0.2|
|tsp225|0.23_±_0.1|0.29_±_0.1|**0.20**|0.24_±_0.2|
|a280|0.16_±_0.1|**0**|0.10_±_0.1|0.91_±_0.4|
|pcb442|2.10_±_0.5|**0.59**_±_0.1|0.80_±_0.5|0.79_±_0.2|
|gr666|**0.93**_±_0.2|1.50_±_0.3|1.19_±_1.3|1.13_±_0.9|
|pr152|0.23_±_0.2|**0.13**|0.16|0.19_±_0.1|
|pr1002|1.78_±_0.6|1.33_±_0.4|1.30_±_0.3|**1.00**_±_0.3|
|pr2392|1.08_±_0.5|**0.87**_±_0.3|1.09_±_0.7|0.92_±_0.3|
|Average gap|0.61|**0.39**|0.45|0.50|



Table 4: Ablation studies based on Qwen7B. Optimality gaps on TSPLIB (%; lower is better). **Bold** marks the best per row. Variance is omitted when it equals 0. 

|Instance|raw|GRPO|Ours|
|---|---|---|---|
|kroA100|**0**|0.21_±_0.1|**0**|
|kroA150|0.80_±_0.1|0.91_±_0.1|**0**|
|kroB100|**0**|**0**|**0**|
|kroB200|2.82_±_1.4|2.02_±_1.1|**0.30**_±_0.1|
|kroC100|0.44_±_0.1|0.10|**0**|
|bier127|2.82_±_1.4|3.01_±_1.1|**1.09**_±_0.2|
|tsp225|5.22_±_3.4|4.01_±_2.4|**0.24**_±_0.2|
|a280|4.82_±_1.4|3.31_±_0.4|**0.91**_±_0.4|
|pcb442|3.00_±_1.9|2.21_±_1.9|**0.79**_±_0.2|
|gr666|8.02_±_5.4|4.82_±_2.2|**1.13**_±_0.9|
|pr152|1.49_±_0.4|1.12_±_0.3|**0.19**_±_0.1|
|pr1002|9.98_±_8.4|5.02_±_2.7|**1.00**_±_0.3|
|pr2392|10.86_±_7.4|8.21_±_7.3|**0.92**_±_0.3|
|Average gap|5.01|4.39|**0.59**|



**Comparison to mainstream proprietary LLMs.** Table 3 contrasts our fine-tuned **Qwen-7B** with three popular closed-source models operating in zero-shot mode (GPT-4o, OpenAI O3, DeepSeek- 

14 

R1). Despite its far smaller size and cost, the fine-tuned model achieves accuracy on par with the strongest proprietary alternatives. 

**Ablation studies.** Table 4 studies the contribution of our dual-reward fine-tuning. Starting from the raw Qwen-7B, we compare (a) vanilla GRPO and (b) our POR+CPR rewards. The dual-reward variant reduces the average gap from 5.01% to 0.59%, and dominates GRPO on every instance. 

**Effect of test-time search.** We next quantify the benefit of test-time search. During inference, the selector may perform a small Monte Carlo search: for each candidate heuristic proposed by the LLM, it rolls out _k_ random completions and takes the average score. We refer to _k_ as the **rollout budget** . Figure 9 plots the optimality gap versus the rollout budget on the pr152 instance. Larger budgets consistently reduce the gap as expected, and our dual-reward fine-tuned selector (POR + CPR) dominates all baselines at any fixed budget. 



Figure 9: Impact of rollout budget on pr152 from TSPLIB [46]. X-axis: Monte Carlo samples per candidate heuristic ( **rollout budget** ; 0 = direct use of the LLM-proposed heuristic with no search). Base model is Qwen-7B. Y-axis: optimality gap (%; Lower is better). 

## **5 Conclusion** 

We have introduced **HeurAgenix** , an end-to-end, LLM-driven hyper-heuristic framework that automatically evolves diverse heuristics and selects among them online. A contrastive, data-driven evolution phase discovers reusable improvement patterns without external solvers, while an adaptive selector—implemented either with an off-the-shelf LLM or a fine-tuned, lightweight model—leverages test-time scaling and a dual-reward mechanism to remain robust under noisy supervision. On standard CO benchmarks, HeurAgenix consistently outperforms existing LLM-based hyper-heuristics and matches or exceeds specialized solvers, demonstrating strong scalability and domain generality. 

Several avenues remain for future work. First, our empirical study has so far been limited to the Qwen-7B backbone, and we will evaluate HeurAgenix across a broader spectrum of model sizes and architectures to assess robustness and cost–performance trade-offs. Then, the current POR relies on a manually chosen positive/negative split, and we plan to devise adaptive, data-driven schemes that adjust these thresholds dynamically during training. Last, while the selector now targets heuristic choice for classical CO tasks, its principle—sequentially picking an operator in a finite operation space with only terminal rewards—naturally extends to more general finite-state Markov Decision Processes(MDP), and exploring this wider class of decision problems is an important next step. 

15 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela, and Marco Protasi. _Complexity and approximation: Combinatorial optimization problems and their approximability properties_ . Springer Science & Business Media, 2012. 

- [3] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- [4] John E Beasley. Or-library: distributing test problems by electronic mail. _Journal of the operational research society_ , 41(11):1069–1072, 1990. 

- [5] Jürgen Branke, Su Nguyen, Christoph W Pickardt, and Mengjie Zhang. Automated design of production scheduling heuristics: A review. _IEEE Transactions on Evolutionary Computation_ , 20(1):110–124, 2015. 

- [6] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling, 2024. 

- [7] Samuel Burer, Renato DC Monteiro, and Yin Zhang. Rank-two relaxation heuristics for max-cut and other binary quadratic programs. _SIAM Journal on Optimization_ , 12(2):503–521, 2002. 

- [8] Edmund Burke, Graham Kendall, Jim Newall, Emma Hart, Peter Ross, and Sonia Schulenburg. Hyperheuristics: An emerging direction in modern search technology. _Handbook of metaheuristics_ , pages 457–474, 2003. 

- [9] Edmund K Burke, Michel Gendreau, Matthew Hyde, Graham Kendall, Gabriela Ochoa, Ender Özcan, and Rong Qu. Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ , 64(12):1695–1724, 2013. 

- [10] Edmund K Burke, Matthew Hyde, Graham Kendall, Gabriela Ochoa, Ender Ozcan, and Rong Qu. A survey of hyper-heuristics. _Computer Science Technical Report No. NOTTCS-TR-SUB-0906241418-2747, School of Computer Science and Information Technology, University of Nottingham_ , 2009. 

- [11] Edmund K Burke, Sanja Petrovic, and Rong Qu. Case-based heuristic selection for timetabling problems. _Journal of Scheduling_ , 9:115–132, 2006. 

- [12] Lingjiao Chen, Jared Quincy Davis, Boris Hanin, Peter Bailis, Ion Stoica, Matei Zaharia, and James Zou. Are more llm calls all you need? towards scaling laws of compound inference systems, 2024. 

- [13] Edoardo Conti, Vashisht Madhavan, Felipe Petroski Such, Joel Lehman, Kenneth Stanley, and Jeff Clune. Improving exploration in evolution strategies for deep reinforcement learning via a population of noveltyseeking agents. _Advances in neural information processing systems_ , 31, 2018. 

- [14] William J Cook, William H Cunningham, William R Pulleyblank, and Alexander Schrijver. Combinatorial optimization. _Unpublished manuscript_ , 10:75–93, 1994. 

- [15] Á Corberán, J Peiró, V Campos, F Glover, and R Martí. Optsicom project. `https://grafo.etsii. urjc.es/optsicom` , 2006. 

- [16] Vinicius Renan de Carvalho, Ender Özcan, and Jaime Simão Sichman. Comparative analysis of selection hyper-heuristics for real-world multi-objective optimization problems. _Applied Sciences_ , 11(19):9153, 2021. 

- [17] Valdivino Alexandre de Santiago Junior, Ender Özcan, and Vinicius Renan de Carvalho. Hyper-heuristics based on reinforcement learning, balanced heuristic selection and group decision acceptance. _Applied Soft Computing_ , 97:106760, 2020. 

- [18] DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. 

- [19] Marco Dorigo, Mauro Birattari, and Thomas Stutzle. Ant colony optimization. _IEEE computational intelligence magazine_ , 1(4):28–39, 2007. 

- [20] John H Drake, Ahmed Kheiri, Ender Özcan, and Edmund K Burke. Recent advances in selection hyperheuristics. _European Journal of Operational Research_ , 285(2):405–428, 2020. 

16 

- [21] Russell Eberhart and James Kennedy. Particle swarm optimization. In _Proceedings of the IEEE international conference on neural networks_ , volume 4, pages 1942–1948. Citeseer, 1995. 

- [22] Paola Festa, Panos M Pardalos, Mauricio GC Resende, and Celso C Ribeiro. Randomized heuristics for the max-cut problem. _Optimization methods and software_ , 17(6):1033–1058, 2002. 

- [23] Michael Figurnov, Maxwell D Collins, Yukun Zhu, Li Zhang, Jonathan Huang, Dmitry Vetrov, and Ruslan Salakhutdinov. Spatially adaptive computation time for residual networks. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 1039–1048, 2017. 

- [24] Gerd Gigerenzer and Wolfgang Gaissmaier. Heuristic decision making. _Annual review of psychology_ , 62(1):451–482, 2011. 

- [25] Google. Or-tools. `https://developers.google.com/optimization` . 

- [26] Alex Graves. Adaptive computation time for recurrent neural networks. _arXiv preprint arXiv:1603.08983_ , 2016. 

- [27] Boxin Guan, Yuhai Zhao, Ying Yin, and Yuan Li. A differential evolution based feature combination selection algorithm for high-dimensional data. _Information Sciences_ , 547:870–886, 2021. 

- [28] Qingchun Hou, Jingwei Yang, Yiqiang Su, Xiaoqing Wang, and Yuming Deng. Generalize learned heuristics to solve large-scale vehicle routing problems in real-time. In _The Eleventh International Conference on Learning Representations (ICLR)_ , 2023. 

- [29] De-Shuang Huang, Kang-Hyun Jo, Junfeng Jing, Prashan Premaratne, Vitoantonio Bevilacqua, and Abir Hussain, editors. _Intelligent Computing Methodologies_ , volume 13395. Springer Cham, 2022. 18th International Conference. 

- [30] Z Iklassov, Y Du, F Akimov, et al. Self-guiding exploration for combinatorial problems. _arXiv preprint arXiv:2405.17950_ , 2024. 

- [31] Zhihao Jia, Oded Padon, James Thomas, Todd Warszawski, Matei Zaharia, and Alex Aiken. Taso: optimizing deep learning computation with automatic generation of graph substitutions. In _Proceedings of the 27th ACM Symposium on Operating Systems Principles_ , pages 47–62, 2019. 

- [32] Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, Honglak Lee, and Lu Wang. Process reward models that think. _arXiv preprint arXiv:2504.16828_ , 2025. 

- [33] Jin-Gyeom Kim and Bowon Lee. Appliance classification by power signal analysis based on multi-feature combination multi-layer lstm. _Energies_ , 12(14):2804, 2019. 

- [34] Yeong-Dae Kwon, Jinho Choo, Byoungjip Kim, Iljoo Yoon, Youngjune Gwon, and Seungjai Min. Pomo: Policy optimization with multiple optima for reinforcement learning. _Advances in Neural Information Processing Systems_ , 33:21188–21198, 2020. 

- [35] Abdesslem Layeb. A novel quantum inspired cuckoo search for knapsack problems. _International Journal of bio-inspired Computation_ , 3(5):297–305, 2011. 

- [36] F Liu, T Xialiang, M Yuan, et al. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [37] Rafael Martí, Abraham Duarte, and Manuel Laguna. Advanced scatter search for the max-cut problem. _INFORMS Journal on Computing_ , 21(1):26–38, 2009. 

- [38] Seyedali Mirjalili, Seyed Mohammad Mirjalili, and Andrew Lewis. Grey wolf optimizer. _Advances in engineering software_ , 69:46–61, 2014. 

- [39] Tor GJ Myklebust. Solving maximum cut problems by simulated annealing. _arXiv preprint arXiv:1505.03068_ , 2015. 

- [40] GL Nemhauser and LA Wolsey. Integer programming and combinatorial optimization. In _Proceedings of the IPCO: International Conference on Integer Programming and Combinatorial Optimization, Houston, TX, USA_ , pages 22–24. Springer, 1998. 

- [41] Alexander Novikov, Ngân Vu~, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. Alphaevolve: A coding agent for scientific and algorithmic discovery, 2025. 

17 

- [42] Christos H Papadimitriou and Kenneth Steiglitz. _Combinatorial optimization: algorithms and complexity_ . Courier Corporation, 1998. 

- [43] Fernando Peres and Mauro Castelli. Combinatorial optimization problems and metaheuristics: Review, challenges, design, and development. _Applied Sciences_ , 11(14):6449, 2021. 

- [44] Daniel J Power and Ramesh Sharda. Model-driven decision support systems: Concepts and research directions. _Decision support systems_ , 43(3):1044–1061, 2007. 

- [45] PUC-Rio. Cvrplib, 2025 Accessed. Available online: `http://vrp.galgos.inf.puc-rio.br/index. php/en/` . 

- [46] Gerhard Reinelt. Tsplib—a traveling salesman problem library. _ORSA journal on computing_ , 3(4):376–384, 1991. 

- [47] B Romera-Paredes, M Barekatain, A Novikov, et al. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995):468–475, 2024. 

- [48] Mike Schulze, Henrik Nehler, Mikael Ottosson, and Patrik Thollander. Energy management in industry–a systematic review of previous findings and an integrative conceptual framework. _Journal of cleaner production_ , 112:3692–3708, 2016. 

- [49] Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du, Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei Koh, and Luke Zettlemoyer. Spurious rewards: Rethinking training signals in rlvr. `https://rethink-rlvr.notion.site/ Spurious-Rewards-Rethinking-Training-Signals-in-RLVR-1f4df34dac1880948858f95aeb88872f` , 2025. Notion Blog. 

- [50] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024. 

- [51] Emilio Singh and Nelishia Pillay. A study of ant-based pheromone spaces for generation constructive hyper-heuristics. _Swarm and Evolutionary Computation_ , 72:101095, 2022. 

- [52] Evgenii Sopov. A selection hyper-heuristic with online learning for control of genetic algorithm ensemble. _International Journal of Hybrid Intelligent Systems_ , 13(2):125–135, 2016. 

- [53] Maciej Swiechowski, Konrad Godlewski, Bartosz Sawicki, and Jacek Ma´ndziuk.<sup>´</sup> Monte carlo tree search: A review of recent modifications and applications. _Artificial Intelligence Review_ , 56(3):2497–2562, 2023. 

- [54] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- [55] Surat Teerapittayanon, Bradley McDanel, and Hsiang-Tsung Kung. Branchynet: Fast inference via early exiting from deep neural networks. In _2016 23rd international conference on pattern recognition (ICPR)_ , pages 2464–2469. IEEE, 2016. 

- [56] J.J. van Hoorn. _Dynamic Programming for Routing and Scheduling: Optimizing Sequences of Decisions_ . Phd-thesis - research and graduation internal, Vrije Universiteit Amsterdam, 2016. Naam instelling promotie: VU Vrije Universiteit Naam instelling onderzoek: VU Vrije Universiteit. 

- [57] Christos Voudouris, Edward PK Tsang, and Abdullah Alsheddy. Guided local search. In _Handbook of metaheuristics_ , pages 321–361. Springer, 2010. 

- [58] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. _arXiv preprint arXiv:2203.11171_ , 2022. 

- [59] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- [60] Jiaheng Wei, Zhaowei Zhu, Hao Cheng, Tongliang Liu, Gang Niu, and Yang Liu. Learning with noisy labels revisited: A study using real-world human annotations, 2022. 

18 

- [61] Yaoxin Wu, Wen Song, Zhiguang Cao, Jie Zhang, and Andrew Lim. Learning improvement heuristics for solving routing problems. _IEEE transactions on neural networks and learning systems_ , 33(9):5057–5069, 2021. 

- [62] Z Xiao, D Zhang, Y Wu, et al. Chain-of-experts: When llms meet complex operations research problems. In _The Twelfth International Conference on Learning Representations (ICLR)_ , 2023. 

- [63] H Ye, J Wang, Z Cao, et al. Reevo: Large language models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ , 2024. 

- [64] Y Zhang, H Wang, S Feng, et al. Can llm graph reasoning generalize beyond pattern memorization? _arXiv preprint arXiv:2406.15992_ , 2024. 

- [65] Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B Brown, Alec Radford, Dario Amodei, Paul Christiano, and Geoffrey Irving. Fine-tuning language models from human preferences. _arXiv preprint arXiv:1909.08593_ , 2019. 

19 

## **A Heuristic Format** 

In order to facilitate dynamic heuristic switching, all heuristics within the heuristic pool adhere to a uniform format. Each heuristic is implemented as a Python function, characterized by the following structure: 

Nearest Neighbor Heuristic 

```
defnearest_neighbor_f91d (problem_state :dict ,algorithm_data :dict ,
** kwargs)->Tuple[Operator ,dict ]:
""" ...
Args:
...
Returns:
Tuple[Operator ,dict ]:...
"""
#Retrievenecessarydatafromproblem_state
...
#Ifthecurrentsolutionisempty ,startfromthefirstunvisited
node.
ifnotcurrent_solution .tour:
start_node=unvisited_nodes [0]
returnAppendOperator (node=start_node),{}
#Findthenearestneighbortothelastvisitednode.
nearest_node=None
min_distance=float(’inf’)
fornodeinunvisited_nodes :
distance=distance_matrix [last_visited ][ node]
ifdistance<min_distance:
nearest_node=node
min_distance=distance
position=len( current_solution .tour)
returnInsertOperator(node=nearest_node ,position=position),{}
```

Some additional remarks: 1. The function name ends with a unique 4-digit identifier ( `f91d` in this example) to avoid naming conflicts. 

2. The input consists of `problem_state` , and `algorithm_data` , which store problem state, and control parameters, respectively. 

The output consists of the current solution’s operation and additional information. In this example, `AppendOperator(node)` adds a node to the end of the current tour and no more information need be passed. Other TSP heuristics may use `InsertOperator` , `SwapOperator` , `ReverseSegmentOperator` , etc. 

## **B Initial Heuristic Generation** 

For CO problems, the evolutionary process requires initialial seed heuristic algorithms. These can be manually crafted or be generated by HeurAgenix. For classic heuristics, HeurAgenix can **generate from LLM** , where heuristics are produced using the internal knowledge of language models. HeurAgenix can also **learn from literature** , which involves reading abstracts to determine relevance, selecting interesting sections, and then generating heuristics based on the information extracted from relevant sections. When dealing with new problems, HeurAgenix can **transfer heuristics from known problems** . The detailed steps for transferring heuristics from related problems are as follows: 

**Decompose new and known problems** : The LLM decomposes both the new problem and source problems into their respective components. 

**Match components** : The LLM compares the components of the new problem with those of known problems to determine if heuristics from these problems can be leveraged. 

**Analyze heuristics from known problems** : If applicable, the LLM reads the heuristics from these known problems. 

**Evaluate and transfer** : For each heuristic, if the LLM determines it is transferable, it translates the 

20 

components and begins the transfer process; otherwise, it skips this heuristic. 

## **C Heuristic Evolution Example** 

The following diff listings capture the full five-rounds evolution (see Fig. 3) of the nearest neighbor heuristic for the TSP. Lines prefixed with “–” (rendered in red) were removed, while lines prefixed with “+” (rendered in green) were introduced. 

### Evolution Round 1: Adjust Initial Node 

```
ifnotcurrent_solution.tour:
-start_node=unvisited_nodes[0]
+avg_distances=[
+np.mean([distance_matrix[i][j]
+forjinrange(node_num)ifi!=j
+])
+foriinrange(node_num)
+]
+sub_central_node=np.argsort(avg_distances)[1]
+start_node=min(unvisited_nodes,
+key=lambdanode:
+distance_matrix[sub_central_node][node])
...
```

### Evolution Round 2: Evaluate Node Selection 

```
fornodeinunvisited_nodes:
-score=distance_matrix[last_visited][node]
+future_cost=sum([
+distance_matrix[node][unvisited]
+forunvisitedinunvisited_nodesifunvisited!=node
+])
+immediate_cost=distance_matrix[last_visited][node]
+score=immediate_cost+
+problem_state["visited_num"]/node_num/node_num*future_cost
ifdistance<best_score:
```

### Evolution Round 3: Adjust Insert Location 

```
fornodeinunvisited_nodes:
future_cost=sum([
distance_matrix[node][unvisited]
forunvisitedinunvisited_nodes
ifunvisited!=node
```

- `])` 

```
-score=immediate_cost+
-
problem_state["visited_num"]/node_num/node_num*future_cost
+foriinrange(len(current_solution.tour)+1):
+prev_node=current_solution.tour[i-1]
+next_node=current_solution.tour[i]
+immediate_cost=distance_matrix[prev_node][node]+
+distance_matrix[node][next_node]-
+distance_matrix[prev_node][next_node]
+position=i
...
```

Evolution Round 4: Limit Candidate Nodes 

21 

```
...
+threshold_factor=kwargs.get("threshold_factor",0.70)
```

```
+percentage_range=kwargs.get("percentage_range",0.20)
```

- `+ # Calculate average distance from the last visited node to unvisited nodes` 

- `+ avg_distance = np.mean([` 

- `+ distance_matrix[last_visited][node] for node in unvisited_nodes` 

```
+])
```

```
+#Findnearestunvisitednodetothelastvisitednode
```

- `+ nearest_node = min(unvisited_nodes,` 

- `+ key=lambda node: distance_matrix[last_visited][node] + )` 

```
+nearest=distance_matrix[last_visited][nearest_node]
```

- `+ # Prioritize inserting the nearest node if its distance is significantly shorter` 

```
+ifnearest<threshold_factor*avg_distance:
```

- `+ return InsertOperator(node=nearest_node, position=len(current_solution. tour))` 

```
+#Evaluatenodeswithcomparabledistances
```

```
+comparable_nodes=[node
```

- `+ for node in unvisited_nodes` 

```
+ifdistance_matrix[last_visited][node]<=(1+percentage_range)*
nearest
```

```
+]
```

- `for node in unvisited_nodes:` 

- `+ for node in comparable_nodes: ...` 

Evolution Round 5: Periodic Apply 2-opt 

```
...
+apply_2opt_frequency=kwargs.get("apply_2opt_frequency",5)
+N=len(current_solution.tour)
+iflen(current_solution.tour)>2:
+iflen(current_solution.tour)%apply_2opt_frequency==0:
+best_delta=0
+best_pair=None
+foriinrange(N-1):
+forjinrange(i+2,N):
+ifj==N-1andi==0:
+continue
+a=current_solution.tour[i]
+b=current_solution.tour[(i+1)%N]
+c=current_solution.tour[j]
+d=current_solution.tour[(j+1)%N]
+current_cost=distance_matrix[a][b]+distance_matrix[c][d]
+new_cost=distance_matrix[a][c]+distance_matrix[b][d]
+delta=new_cost-current_cost
+ifdelta<best_delta:
+best_delta=delta
+best_pair=(i+1,j)
+ifbest_pair:
+returnReverseSegmentOperator([best_pair]),{}
...
```

22 

## **D Monte Carlo Evaluation Strategy** 

The Monte Carlo Evaluation Strategy aims to evaluate the effectiveness of heuristic algorithms by simulating their performance across multiple problem states. This strategy involves running a series of tests where each heuristic algorithm is assessed based on its ability to improve the solution quality from a given state. The process ensures that each heuristic is tested in a consistent environment, allowing for a fair comparison of their relative strengths and weaknesses. 

As shown in Algorithm 3, the pseudocode outlines the detailed steps involved in this strategy: 

**Algorithm 3** Monte Carlo Evaluation Strategy 

**Input** problem instance _d_ with initial state _z_ 0; test heuristic _H_ test; heuristic pool _H_ ; application frequency _M_ ; number of evaluations _T_ **Output** estimated quality _QH_ test 

- 1: Initialize list _metrics ←_ [ ] 

- 2: **for** t **do** = 1 ... T 

- 3: Apply _H_ test exactly _M_ times to _z_ 0 to obtain _z_ 1 

- 4: _z_<sup>_′_</sup> _← z_ 1 

- 5: **while** the selected heuristic continues to improve the solution **do** 

- 6: Randomly choose _H ∈H_ 

- 7: Apply _H_ once to update _z_<sup>_′_</sup> 

- 8: **end while** 

- 9: Append the final-solution metric to _metrics_ 

- 10: **end for** 

- 11: _QHtest ←_ mean( _metrics_ ) 

- 12: **return** _QHtest_ 

## **E Detailed Parameter Settings** 

This section introduces the detailed experiment settings including heuristic evolution and problem solving. 

- **Experiment platform** 

   - OS: GNU/Linux 

   - kernel: 5.15.0-121-generic 

   - Architecture: x86_64 

   - Processor: Intel(R) Xeon(R) 

   - GPU: 4 × NVIDIA RTX A6000 (48G) 

   - CUDA: 12.2 

- **LLM parameters** 

   - Model: GPT-4o_2024-11-20(2024-05-01-preview) 

   - Model: OpenAI-o3_2025-04-16(2024-05-01-preview) 

   - Model: DeepSeek-R1 

   - Model: Qwen2.5-7B-Instruct-1M 

   - Temperature: 0.7 

   - Top-p: 0.95 

   - Max tokens: 1600 

- **Evolution parameters** 

   - Max API calls for each problem: 2000 

   - Train size for each problem: 20 

   - Max perturbation trials _P_ : 1000 

   - Perturbation ratio (|K| / N): 0.1 

   - Max refinement iterations _T_ : 5 

- **Solving parameters** 

   - Time limitation: 2 hours 

23 

   - Selection frequency (M): 5 

   - Monte Carlo search times: 10 

   - Problem state context length: 1000 

- **Fine-tuning model parameters** 

   - LoRA Rank ( _α_ ): 32 

   - Optimizer: Paged AdamW (8-bit) (‘paged_adamw_8bit‘) 

   - Learning Rate: 1 _×_ 10<sup>_−_6</sup> 

   - Adam _β_ 1: 0.9 

   - Adam _β_ 2: 0.99 

   - Weight Decay: 0.1 

   - Learning Rate Scheduler: Cosine (‘cosine‘) 

   - Warmup Ratio: 0.1 

   - Max. Gradient Norm: 0.1 

   - Mixed Precision: BF16 (if supported by hardware, else FP16) 

   - Per-Device Training Batch Size: 1 

   - Gradient Accumulation Steps: 1 

   - Number of Training Epochs: 1 

   - Maximum Training Steps: -1 (disabled; training duration set by epochs) 

   - Inference Utility for Generation: vLLM (enabled via ‘use_vllm=True‘) 

   - Generations per Prompt ( _NG_ ): 12 

   - Max. Prompt Length: 2048 tokens 

   - Max. Completion Length: 768 tokens 

- **TSP** 

   - Data source: `http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/` 

   - Train instances: 20 generated instances 

   - Validation instances: brg180, eil101, gr202, pr124, pr152, rd100, u159 

   - Test instances: kroA100, kroA150, kroB100, kroB200, kroC100, bier127, tsp225, a280, pcb442, gr666, pr1002, pr2392 

   - Basic heuristics: cheapest insertion, farthest insertion, greedy algorithm, greedy randomized adaptive search procedure grasp, insertion heuristics, nearest insertion, nearest neighbor, random pairwise insertion, 2opt, 3opt 

   - Problem states: average_distance, min_distance, max_distance, std_dev_distance, node_num, current_path_length, remaining_nodes, current_cost, average_edge_cost, last_edge_cost, std_dev_edge_cost, solution_validity, min_edge_cost_remaining, max_edge_cost_remaining 

   - Operators: AppendOperator, InsertOperator, SwapOperator, ReverseSegmentOperator, RelocateOperator 

- **CVRP** 

   - Data source: `http://vrp.galgos.inf.puc-rio.br/index.php/en/` 

   - Train instances: 20 generated instances 

   - Validation instances: A-n63-k10, B-n67-k10, E-n76-k10, F-n45-k4, M-n101-k10, P-n70-k10, X-n101-k25 

   - Test instances: A-n80-k10, B-n78-k10, E-n101-k14, F-n135-k7, M-n200-k17, P-n101-k4 

   - Basic heuristics: farthest insertion, greedy, min cost insertion, nearest neighbor, node shift between routes, petal algorithm, saving algorithm, 2 opt, 3 opt 

   - Problem states: average_demand, demand_variance, upper_triangle_indices, upper_triangle_distances, average_distance, max_distance, min_distance, distance_variance, vehicle_capacity_utilization, node_to_vehicle_ratio, average_route_length, max_route_length, min_route_length, std_dev_route_length, average_route_cost, total_demand_served, average_vehicle_load, average_remaining_vehicle_capacity, number_of_unvisited_nodes, average_unvisited_node_demand, total_remaining_demand 

   - Operators: AppendOperator, InsertOperator, SwapOperator, ReverseSegmentOperator, RelocateOperator, MergeRoutesOperator 

- **MKP** 

   - Data source: `https://people.brunel.ac.uk/$\sim$mastjjb/jeb/orlib/files/` 

   - Train instances: 20 generated instances 

24 

   - Validation instances: gmknap1_1 _∼_ mknap1_7 

   - Test instances: mknapcb1_1 _∼_ mknapcb1_5, mknapcb4_1 _∼_ mknapcb4_5 

   - Basic heuristics: block flip, greedy by cost benefit, greedy by density, greedy by least remaining capacity, greedy by profitto weight ratio, greedy by profit, greedy by resource balance, greedy by weight, greedy improvement, k flip, single swap heuristic, 2 opt 

   - Problem states: average_profit, profit_variance, average_weight_per_resource, weight_variance_per_resource, total_weights, capacity_to_weight_ratio, weights_with_epsilon, profit_to_weight_ratio, solution_density, average_remaining_capacity, remaining_capacity_variance, total_remaining_items, feasibility_ratio, utilized_capacity_ratio, included_items, included_profits, item_profitability_in_solution 

   - Operators: ToggleOperator, AddOperator, RemoveOperator, SwapOperator, FlipBlockOperator 

- **JSSP** 

   - Data source: `https://people.brunel.ac.uk/$\sim$mastjjb/jeb/orlib/files/` 

   - Train instances: 20 generated instances 

   - Validation instances: LA21 _∼_ LA30 

   - Test instances: LA01 _∼_ LA20 

   - Basic heuristics: first come first served, least work remaining, longest job next, longest processing time first, most work remaining, shift operator, shortest job next, shortest processing time first, 2opt, 3opt 

   - Problem states: average_operation_time, max_operation_time, min_operation_time, std_deviation_operation_time, job_operation_time_range, average_job_length, max_job_length, min_job_length, machine_utilization, job_diversity, num_finished_jobs, num_unfinished_jobs, average_job_completion, max_job_completion_time, min_job_completion_time, std_dev_job_completion_time, average_machine_completion, max_machine_completion_time, min_machine_completion_time, std_dev_machine_completion_time, average_idle_time_per_machine, proportion_of_finished_jobs, proportion_of_unfinished_jobs 

   - Operators: AdvanceOperator, SwapOperator, ReverseSequenceOperator, ShiftOperator 

- **MaxCut** 

   - Data source: `https://grafo.etsii.urjc.es/optsicom/maxcut.html` 

   - Train instances: 20 generated instances 

   - Validation instances: g11 _∼_ g20 

   - Test instances: g1 _∼_ g10 

   - Basic heuristics: balanced cut, greedy swap, highest delta edge, highest delta node, highest weight edge, most weight neighbors, multi swap 2, simulated annealing 

   - Problem states: average_node_degree, edge_density, average_edge_weight, max_edge_weight, min_edge_weight, standard_deviation_edge_weight, weighted_degree_distribution, imbalance_ratio, cut_value, average_cut_edge_weight, selected_nodes_ratio, unselected_nodes_ratio, internal_edges, edge_weight_variance_within_sets, boundary_nodes, boundary_node_ratio 

   - Operators: InsertNodeOperator, InsertEdgeOperator, SwapOperator, DeleteOperator 

## **F Detailed Experiment Results** 

This appendix complements the main text with complete, per-instance results. We first report the performance achieved after heuristic evolution (Section F.1); we then present the full outcomes of the problem solving stage when an LLM acts as the online selector (Section F.2). Unless otherwise noted, lower values indicate better solutions, and all gaps are expressed in percent relative to upper bound or best known. 

### **F.1 Detailed Evolution Results** 

The tables below list the optimality gaps obtained by the original seed heuristics and by their evolved counterparts generated by HeurAgenix. Because the public interfaces of ReEvo and EoH can evolve only the nearest-neighbor heuristic for TSP, comparisons with these two baselines are reported exclusively for that setting. 

25 

Table 5: Per-instance optimality gaps (%; lower is better) **before** and **after** heuristic evolution on all benchmark problems. ReEvo and EoH are included only for TSP–nearest-neighbor due to interface limitations. All heuristics are deterministic; therefore variances are zero. 

|TSP<br>kroA100|Cheapest insertion<br>1925|Evolved<br>616|Farthest insertion<br>1645|Evolved<br>912|Nearest neighbor<br>3066|Evolved (Ours<br>45|)<br>EoH<br>981|ReEvo<br>1211|
|---|---|---|---|---|---|---|---|---|
|kroA150|.<br>16.27|.<br>8.22|.<br>14.04|.<br>8.34|.<br>31.69|.<br>10.62|.<br>16.12|.<br>11.33|
|kroB100|15.93|10.86|10.96|10.86|26.4|9.49|14.99|14.49|
|kroB200|223|1181|1773|1181|1476|102|1605|1602|
|kroC100|.<br>29.01|.<br>10.79|.<br>4.98|.<br>10.79|.<br>26.8|.<br>7.02|.<br>17.63|.<br>12.41|
|bier127<br>225|21.87<br>1812|8.55<br>748|12.89<br>1449|8.55<br>748|25.62<br>2835|9.26<br>515|19.04<br>1786|16.44<br>134|
|tsp<br>a280|.<br>23.85|.<br>10.04|.<br>13.07|.<br>10.04|.<br>22.55|.<br>8.27|.<br>19.68|.<br>14.91|
|pcb442|22.31|10.81|18.86|10.81|22.02|12.92|15.42|16.42|
|gr666<br>|17.7<br>|9.41<br>|19.19<br>|9.41<br>|24.67<br>|12.63<br>|16.8<br>|19.74<br>|
|pr152|11.28|6.47|6.6|2.41|16.31|4.36|16.55|14.83|
|pr1002|1956|1108|2501|1108|2782|1067|2448|2017|
|pr2392|.<br>21.7|.<br>15.02|.<br>28.82|.<br>15.02|.<br>21.99|.<br>12.68|.<br>18.49|.<br>24.93|
|average|19.94|9.75|15.62|9.67|24.59|9.06|17.15|15.94|
|CVRP<br>A-n80-k10|Cheapest insertion<br>20.6|Evolved<br>18.67|Farthest insertion<br>29.57|Evolved<br>24.12|Nearest neighbor<br>33.26|Evolved<br>20.6|||
|B-n78-k10|4292|226|3694|2293|4398|4292|||
|E-n101-k14|.<br>39.93|.<br>25.21|.<br>85.1|.<br>25.02|.<br>55.39|.<br>39.93|||
|F-n135-k7|41.82|45.87|23.84|22.34|54.22|41.82|||
|M-n200-k17<br>|36<br>|24.94<br>|104<br>|36.55<br>|56<br>|36<br>|||
|P-n101-k4|38.03|16.89|30.1|24.38|49.93|38.03|||
|average|36.55|25.70|51.59|30.56|48.80|36.55|||
|MKP|Greedy by profit|Evolved|Greedy by weight|Evolved|Greedy by density|Evolved|||
|mknapcb11|20.63|3.39|27.23|7.71|7.71|4.05|||
|_<br>mknacb12|1807|343|3344|459|459|101|||
|p_<br>mknapcb1_3|.<br>21.31|.<br>4.3|.<br>34.62|.<br>4.11|.<br>4.11|.<br>0.98|||
|mknapcb14|13.51|6.19|28.75|16.6|16.6|3.72|||
|_<br>mknapcb1_5<br>|13.58<br>|4.82<br>|27.99<br>|8.19<br>|8.19<br>|2.76<br>|||
|mknapcb4_1|14.13|6.22|30.01|6.57|6.57|2.23|||
|mknapcb42|23.9|4.67|31.02|6.12|6.12|4.38|||
|_<br>kb43|2188|6|2625|989|989|248|||
|mnapc_<br>mknapcb4_4|.<br>9.66|7.58|.<br>25.85|.<br>8.96|.<br>8.96|.<br>3.05|||
|mknapcb4_5|10.75|3.61|30.99|7.55|7.55|2.22|||
|average|16.74|5.02|29.62|8.03|8.03|2.69|||
|JSSP|Most work remaining|Evolved|First come first served|Evolved|Shortest processing time first|Evolved|||
|LA01<br>|<br>32.13<br>|40.01<br>|i<br>241.14<br>|24.62<br>|i<br>119.52<br>|24.62<br>|||
|LA02<br>LA03<br>|49.92<br>33.5<br>|28.40<br>34.84<br>|199.54<br>164.49<br>|28.85<br>29.48<br>|196.64<br>78.56<br>|28.85<br>29.48<br>|||
|LA04<br>LA05|69.49<br>12.31|51.36<br>21.75|272.03<br>200|42.2<br>14.17|158.47<br>141.82|42.2<br>14.17|||
|LA06|243|189|22117|1641|15562|1641|||
|LA07|.<br>24.49|.<br>22.92|.<br>192.58|.<br>27.3|.<br>112.13|.<br>27.3|||
|LA08|48.09|22.48|241.6|11.94|191.77|11.94|||
|LA09|3354|1945|22671|2545|17813|2545|||
|LA10|.<br>27.77|.<br>11.9|.<br>253.03|.<br>5.64|.<br>127.77|.<br>5.64|||
|LA11|27|28.4|218.41|29.05|158.92|29.05|||
|LA12<br>|22.81<br>|18.67<br>|232.24<br>|23.77<br>|140.62<br>|23.77<br>|||
|LA13|19.22|24.43|230|16.26|136.61|16.26|||
|LA14|5.42|23.68|243.65|15.87|159.37|15.87|||
|LA15|2519|3596|22717|1947|16156|1947|||
|LA16|.<br>52.7|.<br>19.05|.<br>312.49|.<br>30.16|.<br>265.71|.<br>30.16|||
|LA17<br>|44.77<br>|18.88<br>|399.87<br>|14.03<br>|296.81<br>|14.03<br>|||
|LA18<br>|33.25<br>|50.59<br>|432.19<br>|33.02<br>|257.9<br>|33.02<br>|||
|LA19|41.09|26.84|430.29|24.23|335.63|24.23|||
|LA20|5565|4113|33293|3415|23581|3415|||
|average|.<br>34.13|.<br>27.99|.<br>263.58|.<br>23.30|.<br>180.47|.<br>23.3|||
|MaxCut<br>|Most weight neighbors<br>|Evolved<br>|Highest weight edge<br>|Evolved<br>|Balanced cut<br>|Evolved<br>|||
|g1|5.26|1.56|9.71|1.89<br>|17.13|1.56|||
|g2|4.74|1.72|10.34|1.57|16.77|1.72|||
|g3<br>|5.03<br>|1.73<br>|9.46<br>|1.94<br>|17.57<br>|1.73<br>|||
|g4<br>g5|5.67<br>5.06|2.25<br>1.81|9.38<br>10.93|1.89<br>1.98|17.91<br>16.88|2.25<br>1.81|||
|g6<br>|29.48<br>|11.52<br>|55.05<br>|9.14<br>|100.69<br>|11.52<br>|||
|g7|31.51|9.97|54.74|10.97|104.44|9.97|||
|g8<br>9|32.05<br>2736|10.17<br>949|58.92<br>5725|12.11<br>1066|112.16<br>9688|10.17<br>949|||
|g<br>|.<br>|.<br>|.<br>|.<br>|.<br>|.<br>|||
|g10|26.15|14.3|59.7|9.15|103.7|14.3|||
|average|17.23|6.45|33.55|6.13|60.41|6.45|||



### **F.2 Detailed Problem Solving Results with LLM** 

We next provide exhaustive results for the online-selection phase, where GPT-4o chooses among the evolved heuristic pool. The same baselines as in Table 6 of the main text are included for completeness. 

26 

Table 6: Per-instance optimality gaps (%; lower is better) of all evaluated methods on the five problems. Bold indicates the **best result** , underline the <u>second-best.</u> Values tagged with<sup>_†_</sup> are taken from external sources; variance is omitted when it equals 0 or results are taken from external sources. 

|TSP<br>kroA100|GLS<br>298_±_02|ACO<br>319_±_31|OR-Tools<br>635_±_04|EoH+GLS<br>**000**|ReEvo+GLS<br>**000**|ReEvo+ACO<br>273<br>_±_07|Ours<br>**000**|
|---|---|---|---|---|---|---|---|
|kroA150<br>|. .<br>0.58<br>|. .<br>3.63_±_3.3<br>|. .<br>4.74_±_0.3<br>|**.**<br>**0.00**<br>|**.**<br>**0.00**<br>|.<br>.<br>4.39_±_2.8<br><br>|**.**<br>**0.00**<br>|
|kroB100<br>kroB200|5.59_±_0.8<br>178_±_08|4.58_±_1.9<br>291_±_18|2.6_±_0.1<br>376_±_19|**0.00**<br>038_±_02|**0.00**<br>018|1.13<br>_±_0.3<br>106_±_08|**0.00**<br>**011**|
|kC100|. .<br>71_±_17|. .<br>369_±_19|. .<br>1274_±_02|. .<br>**000**|.<br>**000**|. .<br>358<br>_±_29|**.**<br>**000**|
|ro<br>bier127|. .<br>5.36_±_1.5|. .<br>5.68_±_0.3|. .<br>5.62_±_0.4|**.**<br>0.36|**.**<br>**0.01**|.<br>.<br>11.04_±_3.5|**.**<br>1.29_±_0.6|
|tsp225|2.32_±_0.1|5.05_±_2.9|8.45_±_0.7|0.48|1.15_±_0.3|1.7_±_1.5|**0.23**_±_0.1|
|280|<br>644_±_06|<br>644_±_3|<br>1254_±_10|**012**|<br>**012**|<br>633_±_22|<br>016<br>_±_01|
|a<br>pcb442|. .<br>3.15_±_1.4|. .9<br>3.15_±_2.7|. .<br>7.94_±_1.3|**.**<br>1.06_±_0.1|**.**<br>0.82<br>_±_0.6|. .<br>2.94_±_2.9|.<br>.<br>**0.79**_±_0.2|
|gr666|4.26_±_1.3|4.26_±_1.8|14.38_±_0.2|2.65_±_0.6|1.08<br>_±_0.5|6.89_±_2.0|**0.93**_±_0.2|
|152|<br>189|<br>1371_±_22|<br>292_±_01|<br>179_±_01|<br>189|<br>931_±_30|<br>**019**_±_01|
|pr<br>pr1002|.<br>4.96_±_4.4|. .<br>4.96_±_2.4|. .<br>22.18_±_0.6|. .<br>14.43_±_4.9|.<br>1.89<br>_±_0.6|. .<br>17.96_±_1.8|**.** .<br>**1.78**_±_0.6|
|pr2392|4.74_±_1.1|4.74_±_3.9|8.45_±_1.2|3.87<br>_±_1.4|5.6_±_1.4|6.37_±_2.0|**1.08**_±_0.5|
|average|3.93|5.08|8.67|1.93|0.98|5.80|**0.50**|
|CVRP<br>|OR-Tools<br><br>|ACO<br>|ReEvo+ACO<br>|Ours<br>||||
|A-n80-k10|6.41<br>_±_0.3|34.96_±_3.1|13.34_±_2.9|**3.97**_±_1.3||||
|B-n78-k10|3.69<br>_±_0.2|0.20_±_8.7|11.37_±_5.9|**2.54**_±_1.2||||
|E-n101-k14<br>|11.06<br>_±_0.5<br><br>|49.30_±_2.9<br>|28.68_±_5.8<br>|**10.97**_±_2.9<br>||||
|F-n135-k7|13.43<br>_±_1.3|50.17_±_6.7|17.47_±_5.5|**8.52**_±_1.2||||
|M-n200-k17|14.04<br>_±_0.6|64.16_±_3.9|33.73_±_6.6|**9.88**_±_1.7||||
|P-n101-k4|8.81<br>_±_0.8|59.18_±_2.1|25.11_±_8.4|**3.08**_±_0.2||||
|average|9.57|43.00|21.62|**6.49**||||
|MKP|QICSA(<sup>_†_</sup>)|PSO(<sup>_†_</sup>)|ACO|ReEvo+ACO|Ours|||
|mknapcb11|3.96|7.61|8.67|8.45_±_2.8|**0.33**|||
|_<br>mknapcb1_2<br>|5.74<br>|8.36<br>|9.45<br>|<br>7.97_±_1.8<br>|**0.20**<br>|||
|mknapcb1_3|4.36|7.34|12.07|5.65_±_0.7|**0.15**|||
|mknapcb1_4<br>kb15|3.43<br>474|6.28<br>760|5.41<br>796|5.12_±_1.8<br>551_±_10|**1.23**_±_0.8<br>**072**_±_03|||
|mnapc_<br>|.<br>|.<br>|.<br>|. .<br><br>|**.** .<br>|||
|mknapcb4_1<br>mknapcb42|5.50<br>6.37|9.40<br>9.38|16.05<br>10.39|3.82<br>_±_0.8<br>4.42<br>_±_1.3|**0.55**_±_0.1<br>**1.05**_±_0.1|||
|_<br>kb43|651|937|1212|463<br>_±_09|**062**_±_02|||
|mnapc_<br>mknapcb4_4|.<br>6.13|.<br>8.19|.<br>10.59|.<br>.<br>4.65<br>_±_0.6|**.** .<br>**1.03**_±_0.5|||
|mknapcb4_5|5.85|9.23|14.89|1.79<br>_±_0.1|**0.91**_±_0.6|||
|average|5.26|8.28|10.76|5.20|**0.68**|||
|JSSP<br>|ACO(<sup>_†_</sup>)<br>|PSO(<sup>_†_</sup>)<br>|GWO(<sup>_†_</sup>)<br>|Ours<br>||||
|LA01<br>LA02|**0.00**<br>**0.00**|**0.00**<br>**0.00**|**0.00**<br>**0.00**|**0.00**<br>**0.00**||||
|LA03|436|101|**000**|**000**||||
|LA04|.<br>3.56|.<br>3.56|**.**<br>**0.00**|**.**<br>**0.00**||||
|LA05|**0.00**|**0.00**|**0.00**|**0.00**||||
|LA06<br>|**0.00**<br>|**0.00**<br>|**0.00**<br>|**0.00**<br>||||
|LA07|**0.00**|**0.00**|**0.00**|**0.00**||||
|LA08|**0.00**|**0.00**|**0.00**|**0.00**||||
|LA09|**000**|**000**|**000**|**000**||||
|LA10|**.**<br>**0.00**|**.**<br>**0.00**|**.**<br>**0.00**|**.**<br>**0.00**||||
|LA11<br>LA12|**0.00**<br>**000**|**0.00**<br>**000**|**0.00**<br>**000**|**0.00**<br>**000**||||
|LA13|**.**<br>**0.00**|**.**<br>**0.00**|**.**<br>**0.00**|**.**<br>**0.00**||||
|LA14<br>LA15<br>|**0.00**<br>0.41<br>|**0.00**<br>**0.00**<br>|**0.00**<br>**0.00**<br>|**0.00**<br>**0.00**<br>||||
|LA16<br>LA17|**0.00**<br>**0.00**|6.35<br>3.57|1.16<br>0.77|1.69_±_0.2<br>1.79_±_0.1||||
|LA18|**000**|436|130|024<br>_±_01||||
|LA19|**.**<br>**0.00**|.<br>3.92|.<br>0.36|.<br>.<br>1.19_±_0.2||||
|LA20|**0.00**|1.11|3.88|**0.00**||||
|average|0.42|1.19|0.37|**0.25**||||
|MaxCut<br>|SS(<sup>_†_</sup>)<br>|CirCut(<sup>_†_</sup>)<br>|VNSPR(<sup>_†_</sup>)<br>|Ours<br>||||
|g1|**0.00**|**0.00**|0.03|**0.00**||||
|g2<br>3|**0.00**<br>**000**|0.17<br>001|0.04<br>**000**|0.07<br>009||||
|g<br>g4|**.**<br>**0.00**|.<br>0.11|**.**<br>0.39|.<br>0.44_±_0.1||||
|g5|**0.00**|0.01|0.28|0.22_±_0.1||||
|6|060|**000**|349|**000**||||
|g<br>|.<br>|**.**<br>|.<br>|**.**<br>||||
|g7|1.20|**0.00**|4.99|1.30_±_0.2||||
|g8|1.00|**0.10**|4.89|0.80<br>_±_0.1||||
|g9<br>|0.68<br>|**0.10**<br>|2.73<br>|2.73_±_0.3<br><br>||||
|g10|0.35<br>|**0.20**<br>|4.50<br>|0.35<br>_±_0.1<br>||||
|average|0.38|**0.07**|2.13|0.60||||



27 

