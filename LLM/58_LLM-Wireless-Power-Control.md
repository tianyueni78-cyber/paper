The latest version of this work has been accepted by ICML 2025 Workshop on ML4Wireless, and the revised title is ” _Prompting Wireless Networks: Reinforced In-Context Learning_ _<u>for</u> Power Control”._ 

# Large Language Model (LLM)-enabled In-context Learning for Wireless Network Optimization: A Case Study of Power Control 

Hao Zhou, Chengming Hu, Dun Yuan, Ye Yuan, Di Wu, Xue Liu, _Fellow, IEEE_ , and Jianzhong (Charlie) Zhang, _Fellow, IEEE_ . 

**_Abstract_ —Large language model (LLM) has recently been considered a promising technique for many fields. This work explores LLM-based wireless network optimization via in-context learning. To showcase the potential of LLM technologies, we consider the base station (BS) power control as a case study, a fundamental but crucial technique that is widely investigated in wireless networks. Different from existing machine learning (ML) methods, our proposed in-context learning algorithm relies on LLM’s inference capabilities. It avoids the complexity of tedious model training and hyper-parameter fine-tuning, which is a well-known bottleneck of many ML algorithms. Specifically, the proposed algorithm first describes the target task via formatted natural language, and then designs the in-context learning framework and demonstration examples. After that, it considers two cases, namely discrete-state and continuous-state problems, and proposes state-based and ranking-based methods to select appropriate examples for these two cases, respectively. Finally, the simulations demonstrate that the proposed algorithm can achieve satisfactory performance without updating the LLM model parameters. Such an efficient and low-complexity approach has great potential for future wireless network optimization.** 

**_Index Terms_ —Large language model, in-context learning, network optimization, transmission power control** 

## I. INTRODUCTION 

The envisioned 6G network will be increasingly complicated with diverse application scenarios and novel signal processing techniques, e.g., vehicle-to-everything (V2X), mmWave and THz networks, reconfigurable intelligent surface, etc [1]. The constantly evolving network architecture requires more efficient management schemes, and most existing network optimization methods can be summarized into two main approaches: convex optimization and machine learning (ML) algorithms. Specifically, convex optimization usually needs dedicated problem formulation for each specific task, then transforms the objective function or constraints into convex forms. By contrast, ML algorithms, such as reinforcement learning, have lower requirements for problem formulations, but the tedious model training and fine-tuning indicate a large number of iterations [2]. Therefore, these potential issues, e.g., 

Hao Zhou, Chengming Hu, Dun Yuan, Ye Yuan, and Xue Liu are with the School of Computer Science, McGill University, Montreal, QC H3A 0E9, Canada. (mails:hao.zhou4, chengming.hu, dun.yuan, ye.yuan3@mail.mcgill.ca, xueliu@cs.mcgill.ca). Di Wu is with the School of Electrical and Computer Engineering, McGill University, Montreal, QC H3A 0E9, Canada. (email: di.wu5@mcgill.ca). Jianzhong (Charlie) Zhang is with Samsung Research America, Plano, Texas, TX 75023, USA. (email: jianzhong.z@samsung.com). 

problem-specific transformation and relaxation, hyperparameter tuning, and long training iterations, have become obstacles to further improve the efficiency of next-generation networks. 

Recently, generative AI (GAI) and large language models (LLMs) have provided promising opportunities for network fields [3], e.g., 6G edge intelligence [4], beamforming [5], reconfigurable intelligent surfaces (RISs) [6], wireless network design [7], etc. Motivated by the issues of existing optimization techniques, this work explores LLM-enabled network optimization techniques. It considers base station (BS) power control as a case study, which is a fundamental and critical technique that has been extensively studied by using convex optimization, game theory, reinforcement learning, etc. However, few existing studies have addressed this crucial network optimization problem from a language-related perspective. Such a novel technique has great potential to save human labour for network operations, e.g., i.e., optimizing network performance by using natural language directly. LLMs can also provide detailed explanations for their outputs, helping humans understand complicated 6G networks. 

To this end, this work proposes a novel LLM-enabled incontext learning algorithm for optimization tasks. In-context learning indicates learning from language-based descriptions and demonstrations, which has multiple advantages [8]: 1) In-context learning relies on LLM’s inference process, and it avoids the complexity of updating the LLM model parameters, saving considerable computational resources; 2) Incontext learning allows natural language-based task design and implementation, and the operator can easily formulate the target task using human language and instructions. In addition, prompt engineering only requires forward passing of the model without the need for backpropagation. Therefore, the fast implementation and low response time can more efficiently handle network dynamics. 

In particular, our proposed technique first designs a natural language-based task description, i.e., task goal, definition, and rules. The formatted task description, along with a set of selected examples, will become the prompt input for the LLM model. Then, the LLM model can utilize the task description and advisable examples to generate a decision based on the current environment state. Different from existing LLM-enabled network optimization studies [7], we propose a novel experience pool framework. It will collect the previous experience and decisions of LLMs, serving as references for 

1 

future decision-making. In addition, examples are crucial for in-context learning. Distinct from prior studies [5], [7], we further propose two novel example selection methods, namely state-based and ranking-based approaches, for discrete-state and continuous-state problems, respectively. With experience pools and proper example selection, LLMs can utilize the accumulated experience and find hidden patterns from examples, making optimal decisions accordingly. 

The core contribution of this work is that we proposed a LLM-enabled in-context learning technique for network optimization, which can learn from the language-based task descriptions and environment interactions. It overcomes the tedious model training and parameter fine-tuning processes, which are usually time-consuming in conventional ML algorithms. We further evaluate the proposed algorithm with various LLMs, e.g., Llama3-8b-instruct, Llama3-70b-instruct, and GPT-3.5 turbo, and the simulations prove that the proposed algorithm can achieve satisfactory performance. 

## II. SYSTEM MODEL 

## _A. Power Control Problem Formulation_ 

This section introduces a BS power minimization problem, serving as a case study of the proposed in-context learning algorithm. Considering a BS with _Ub_ users, the achievable data rate _Cb,u_ between BS _b_ and user _u_ is defined by 



where _Kb_ is the total number of resource blocks (RBs) in BS _b_ , _dk_ is the bandwidth of RB _k_ , _pb,k_ indicates the transmission power of BS _b_ on RB _k_ , _hb,k,u_ defines the channel gain between BS _b_ and user _u_ on RB _k_ , and _N_ 0 is the noise power density. For the RB allocation, _γb,k,u ∈{_ 0 _,_ 1 _}_ indicates whether RB _k_ is allocated to the transmission for user _u_ . For the interference, _B−b_ represent the set of adjacent BSs except for BS _b_ , _pb′,k′hb′,k′,u′γb′,k′,u′_ defines the inter-cell interference, and we assume orthogonal frequency-division multiplexing is applied to eliminate intra-cell interference. This work aims to minimize the BS transmission power and meanwhile satisfy the average data rate constraint [9]: 





where _Pb_ is the total transmission power of BS _b_ and _Pb_ =<sup>�</sup><sup>_K_</sup> _k_ =1<sup>_bpb,k_,</sup><sup>_pb,k_hasbeendefinedinequation(1)asthe</sup> transmission power of RB _k_ , _Pmax_ is the maximum power, _Ub_ is the total number of users, and _Cmin_ is the average achievable data rate constraint. We assume _Pb_ is equally allocated to all RBs, and a proportional fairness method is used for RB allocation, which has been widely used as a classic approach. Then we can better focus on LLM features. 

## _B. Language-based Power Control Task Description_ 

Problem (2) has been extensively investigated in existing studies, but this work differs from previous works by presenting a unique view from the perspective of LLM-enabled network optimization. Instead of defining specific equations as in (2), here we use natural language to describe the optimization task. Specifically, the defined task description is shown below, which will further be used to prompt LLMs: 

## Task description for BS transmission power control 

**Task goal** : You have a decision-making task for base station power control, and you need to select between 4 power levels from 1 to 4. 

**Task definition** : You have to consider the specific user number of each case, which is the “BS user number”. Following are some examples _{Example_ _<u>set}</u>_ . Now I will give you a new condition to solve, the current BS user number is _{Num BS_ _<u>user}</u>_ . **Rules** : Now please select from “level 1”, “level 2”, “level 3”, and “level 4” based on the above examples. 

In particular, the _Task_ _<u>goal</u>_ first specifies a “ _decisionmaking task for base station power control_ ”, and the goal is to “ _select between 4 power levels_ ”. Then the _Task definition_ introduces the environment states we need to consider. For example, this work assumes the total user numbers may change dynamically, and then the LLM has to consider the “ _user number_ ” of each case. After that, the example set _Et_ is included by “ _Following are some examples...._ ”, and we provide a new condition for the LLM to solve with the current user number _Ub_ . Finally, we set extra reply rules such as “ _select from ... based on the above examples_ ”, indicating the LLM to focus on the decision-making process. Such a definition provides a standard template for addressing many optimization tasks by including goals, definitions, and rules. 

## III. IN-CONTEXT LEARNING-BASED OPTIMIZATION ALGORITHM 

## _A. In-context Learning_ 

In-context learning refers to the process that LLMs can learn from formatted natural language such as task descriptions and task solution demonstrations, to improve the performance on target tasks. In-context learning can be defined as [8] 



where _Dtask_ is the task description and query, _Et_ is the set of examples at time _t_ , _st_ is the environment state at time _t_ that is associated with the target task, _LLM_ indicates the LLM model, and _at_ is the LLM output. Here we expect the LLM can utilize the initial task description _Dtask_ , learn from the example set _Et_ , and then make decision _at_ based on current environment state _st_ of the target task. 

The LLM’s in-context learning capabilities can be explained by implicit fine-tuning according to [10]. Specifically, LLMs 

2 



Fig. 1: Overall design of the proposed LLM-enabled in-context learning for transmission power control. 

will produce meta-gradients based on given examples _E_ by forward computation, and then the meta-gradients are applied by using the attention mechanism to build an in-context learning model [10]: 



where **q** is the query vector in the attention mechanism, _WZSL_ indicates the zero-shot learning case without examples, ∆ _W_ ICL is the updated weight when examples _E ∈E_ are provided by in-context learning. 

## _B. Examples and Optimization Framework Design_ 

The analyses in Section III-A show that examples are of great importance in in-context learning, which will directly affect the ∆ _W_ ICL values. Here we define an example by 



where _s_ and _a_ are environment state and decision, respectively. Inspired by reinforcement learning, we further define a reward value to evaluate the decision _a_ by 



where _Ptarget_ is a target power consumption, and _Pb_ has been defined in problem (2) as the total power consumption of BS _b_ . _β_ is a penalty term, which is only applied when constraint (2c) is not satisfied. Then, _r_ provides a comprehensive metric to evaluate the selected decision _a_ under environment state _s_ . 

Fig.1 shows the overall design of the proposed in-context learning algorithm. Specifically, the above task description _Dtask_ , current environment state _st_ , and selected examples _Et_ are integrated as input prompt as defined in equation (3), and then the LLM model will generate a power control decision _at_ based on _st_ and the experiences in _Et_ . Then, the decision _at_ is implemented, the achieved data rate _Cb,u_ is collected, and the reward _rt_ is calculated as equation (6). _Et_ = _{st, at, rt_ ( _st, at_ ) _}_ becomes a new example in the 

accumulated experience pool _Epool_ . After that, we considered two scenarios, namely discrete and continuous state problems, and proposed state-based and ranking-based example selection methods. Based on the next environment state _st_ +1, a new example set _Et_ +1 is selected, and the selected examples are inserted into the task description with _st_ +1, becoming a new prompt for the LLM model to generate _at_ +1. 

## _C. State-based Example Selection for Discrete States_ 

Selecting appropriate examples is critical for in-context learning. To improve the quality of selected examples, this subsection introduces a state-based example selection method for problems with discrete environment states. Considering a target task with environment state value _starget_ , the set of relevant examples can be identified by 



where _Epool_ is the accumulated experience pool in Fig. 3. Given the current state _starget_ , equation (7) provides a practical solution to find the most relevant examples _Erelevant_ . With _Erelevant_ , we can easily select recommended top examples with higher reward, and inadvisable examples with lower reward or violating the minimum data rate constraint in the problem formulation. In addition, we include a well-known epsilon-greedy policy to balance exploration and exploitation. 



where _ϵ_ is a predefined value, and _rand_ is a random number between 0 and 1. Therefore, the random exploration in equation (8) can constantly explore new examples, and then the LLM model can learn from better relevant examples _Erelevant_ to improve the performance. 

_D. Ranking-based Example Selection for Continuous States_ This subsection introduces a ranking-based method to select proper examples for continuous state problems. Specifically, 

3 



## Fig. 2: **The overall procedure of the example-related scheme.** 

continuous states indicate an infinite number of possible examples, and identifying the most relevant and high-quality examples can be challenging. For instance, when using average user-BS distance as an environment state for BS transmission power control with a target task _starget_ , it is unlikely to find a specific existing example _E{s, a, r_ ( _s, a_ ) _}_ with _s_ = _starget_ , since _starget_ is a random number within the BS maximum coverage distance. To this end, we define a new metric _L_ for example selection with continuous states: 



where _L_ ( _E, starget_ ) is a comprehensive metric to evaluate the usefulness of _E_ = _{s, a, r_ ( _s, a_ ) _}_ to the decision-making of _starget_ , and _||s−starget||_ is the _L_<sup>2</sup> norm to define the distance between _s_ and _starget_ . Equation (9) aims to jointly consider the reward and states of example _E_ , and _τ_ is a weighting factor to balance the importance of higher reward _r_ ( _s, a_ ) and more similar states between _s_ and _starget_ . Specifically, a higher reward _r_ ( _s, a_ ) indicates that _E_ includes a good action selection _a_ under environment state _s_ , and meanwhile lower _||s − starget||_ value means the environment state _s_ in _E_ is more similar to _starget_ . Therefore, _L_ ( _E, starget_ ) becomes a comprehensive metric to evaluate the quality of examples in _Epool_ . With _L_ ( _E, starget_ ), we can easily select recommended and inadvisable examples by ranking all elements in _Epool_ . 

## _E. Computational Complexity Analyses_ 

Fig. 2 summarizes the overall procedure of example-related schemes. In particular, the LLM receives the state from the environment, and then uses the examples provided by the experience pool to select actions such as the transmission power level. The implementation results will become a new example for the pool. Meanwhile, no additional computational cost is incurred for example selection, as each new example is simply appended to the accumulated experience pool after implementation. Secondly, for example selection in discrete state problems, it is easy to search the experience pool to identify _s_ = _starget_ . For continuous states, we calculate the _L_ ( _E, starget_ ) metric for all examples in the pool, and then select the best examples accordingly. Therefore, the cost of example selection follows a linear complexity. Finally, note that the LLM inference time is affected by model architecture, hardware constraints, and task types, and it can also be further optimized by quantization, sparsity exploitation, and architectural innovations. 

## IV. PERFORMANCE EVALUATION 

## _A. Simulation Settings_ 

We consider three adjacent small base stations (SBSs), the user number of each SBS randomly changes from 5 to 15, 

and the SBS’s coverage is 20 meters. The channel gain applies 3GPP urban network models, and 2 cases are evaluated: **Case I** : Discrete states defined by user numbers of each SBS; **Case II** : Continuous states defined by average user-SBS distance, which represents 2 kinds of network optimization problems. Then, the simulation considers 3 main approaches: **1) LLM-based method** applies our proposed technique with various models: Llama3-8b-instruct, Llama3-70b-instruct, GPT-4, and GPT-3.5 turbo. Using LLM models with various sizes and capabilities can better evaluate the performance of our proposed algorithms. We have also evaluated the system performance by ablation studies, e.g., performance without the proposed mechanisms such as experience pool, example selection, and random exploration. In addition, we considered the feedback-based approach in [7] as another baseline. **2) DRL-based method** : We employ DRL as a baseline algorithm, since it has been widely used to address various network optimization problems in many existing studies [2]. **3) Exhaustive search** : We apply exhaustive search method as the optimal baseline, searching for the best decisions exhaustively. 

## _B. Simulation Results_ 

Fig. 3 shows the simulation results and comparisons. Firstly, Fig. 3(a) and 3(b) present the reward and service quality under discrete and continuous state spaces. One can observe that LLMs can achieve higher rewards as the number of episodes increases, and Llama3 LLMs present close performance as the DRL baseline method for discrete and continuous problems. Fig. 3(a) and 3(b) demonstrate that LLMs can learn from previous examples and interactions, and then improve their performance on target tasks iteratively. 

Then, we implement ablation studies in Fig. 3(c). It demonstrates the importance of our proposed techniques, e.g., the experience pool design, the example selection strategies, and exploration policies. Without these designs, the in-context learning technique presents a much lower reward than exhaustive search. It highlights the necessity of our designs in understanding the internal mechanisms of in-context learning technique and LLM-enabled optimization. Meanwhile, the feedback-based method also shows a worse performance. It means that using the feedback from previous implementations solely cannot fully reflect the complexity of a dynamic environment. It can be used to address static optimization problems as introduced in [7], but it cannot handle dynamic optimization problems as defined in our work. 

Moreover, we observe the algorithm performance under different minimum data rate constraints. Fig. 3(d) and 3(e) present the average power consumption and service quality, respectively. As expected, given the limited bandwidth, increasing the minimum data rate constraint leads to higher power consumption and lower service quality for all algorithms. GPT-4, Llama3-8b, and Llama3-70b show a close performance as the task-specific DRL algorithm and exhaustive search baseline. They demonstrate that the proposed in-context learning can adapt to different optimization settings and then adjust their policies to improve the performance of target tasks. 

4 









<!-- Start of picture text -->
(a) Discrete state space: System reward and (b) Continuous state space: System reward and (c) Continuous state space: Average reward com-<br>service quality comparison. service quality comparison. parison under different data rate constraints. (ICL:<br>In-context learning)<br><!-- End of picture text -->









<!-- Start of picture text -->
(d) Continuous state space: Average power (e) Continuous state space: Average service quality (f) Continuous state space: Reward with increasing<br>consumption comparison under different comparison under different data rate constraints. number of examples and and larger spaces.<br>data rate constraints.<br><!-- End of picture text -->

Fig. 3: Simulation results and comparisons 

By contrast, GPT-3.5 shows worse performance than other techniques, which indicates that algorithm performance is also related to specific LLMs. Specifically, GPT-4 and Llama3 represent state-of-the-art LLM designs, while GPT-3.5 is an early and outdated LLM model. 

Finally, Fig. 3(f) evaluated the system performance with enlarged state space and changing number of examples in the prompt. Firstly, one can observe that increasing the number of examples can constantly improve the average reward. However, such improvement becomes less obvious when plenty of examples are provided. On the other hand, increasing the state space means that more examples are needed in the prompt to achieve a satisfactory performance, e.g., more references and experience are needed to make proper decisions. However, it is worth noting that the overall performance is still constantly improving by increasing the number of provided examples, and it finally achieves a comparable performance as the exhaustive search method. 

## V. CONCLUSION 

LLM is a promising technique for future wireless networks, and this work proposes an LLM-enabled in-context learning algorithm for BS transmission power control. The proposed algorithm can handle both discrete and continuous state problems, and the simulations show that it achieves comparable performance as conventional DRL algorithms. This work demonstrates the great potential of in-context learning for handling network management and optimization problems. In 

the future, we will focus on the practical application of LLMs to wireless networks, including operation costs, on-premises deployment, and real-time performances. 

## REFERENCES 

- [1] Z. Zhang, Y. Xiao, Z. Ma, M. Xiao, Z. Ding, X. Lei, G. K. Karagiannidis, and P. Fan, “6g wireless networks: Vision, requirements, architecture, and key technologies,” _IEEE vehicular technology magazine_ , vol. 14, no. 3, pp. 28–41. 

- [2] H. Zhou, M. Erol-Kantarci, Y. Liu, and H. V. Poor, “A survey on modelbased, heuristic, and machine learning optimization approaches in risaided wireless networks,” _IEEE Commu. Surveys & Tutorials_ , 2023. 

- [3] H. Zhou, C. Hu, Y. Yuan, Y. Cui, Y. Jin, C. Chen, H. Wu, D. Yuan, L. Jiang, D. Wu _et al._ , “Large language model (LLM) for telecommunications: A comprehensive survey on principles, key techniques, and opportunities,” _arXiv preprint arXiv:2405.10825_ , 2024. 

- [4] Z. Lin, G. Qu, Q. Chen, X. Chen, Z. Chen, and K. Huang, “Pushing large language models to the 6G edge: Vision, challenges, and opportunities,” _arXiv preprint arXiv:2309.16739_ , 2023. 

- [5] C. Zhang, S. Xiong, M. He, L. Wei, Y. Huang, and W. Zhang, “Generative learning powered probing beam optimization for cell-free hybrid beamforming,” _IEEE Wireless Communications Letters_ , 2024. 

- [6] C. B. Chaaya and M. Bennis, “Ris phase optimization via generative flow networks,” _IEEE Wireless Communications Letters_ , 2024. 

- [7] K. Qiu, S. Bakirtzis, I. Wassell, H. Song, J. Zhang, and K. Wang, “Large language model-based wireless network design,” _IEEE Wireless Communications Letters_ , 2024. 

- [8] Q. Dong, L. Li, D. Dai, C. Zheng, Z. Wu, and et al., “A survey on in-context learning,” _arXiv preprint arXiv:2301.00234_ , 2022. 

- [9] M. Chiang, P. Hande, T. Lan, C. W. Tan _et al._ , “Power control in wireless cellular networks,” _Foundations and Trends® in Networking_ , vol. 2, no. 4, pp. 381–533, 2008. 

- [10] D. Dai, Y. Sun, L. Dong, Y. Hao, S. Ma, Z. Sui, and F. Wei, “Why can gpt learn in-context? language models implicitly perform gradient descent as meta-optimizers,” _arXiv preprint arXiv:2212.10559_ , 2022. 

5 

