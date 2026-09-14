# **OR-Toolformer: Modeling and Solving Operations Research Problems with Tool Augmented Large Language Models** 

**Jianzhang Zhang, Jialong Zhou and Chuang Liu**<sup>**†**</sup> Alibaba Business School, Hangzhou Normal University {zjzhang,liuchuang}@hznu.edu.cn, jialongzhouzj@gmail.com 

## **Abstract** 

Large language models (LLMs) demonstrate strong mathematical reasoning, but reliance on closed-source APIs for OR tasks raises privacy concerns, and training open-source models from scratch incurs high compute costs. We introduce OR-Toolformer, which fine-tunes Llama-3.1-8B-Instruct with a semi-automatic data synthesis pipeline that generates diverse OR problem-answer pairs and augments the model with external solvers to produce API calls. On three of four standard benchmarks, OR-Toolformer achieves up to 80.1% execution accuracy, exceeding size-matched baselines by over 4.3%. In zero-shot evaluation on two unseen OR problem types, it attains 54% average accuracy, a 21 percentage-point improvement over the strongest baseline. These findings validate the efficacy of tool-augmented fine-tuning LLMs for accurate and generalizable OR problem modeling and solving. 

## **1 Introduction** 

Operations Research (OR) offers rigorous methods to formalize and solve complex decision problems in various sectors. OR workflows involve (1) translating natural-language descriptions into mathematical optimization models and (2) obtaining solutions via general-purpose solvers (Petropoulos et al., 2024), yet this pipeline remains dependent on domain expertise, limiting scalability. 

Large language models (LLMs) have demonstrated strong text comprehension and multistep mathematical reasoning on complex benchmarks (Romera-Paredes et al., 2024; Xia et al., 2025), indicating their potential to automate both formulation and solution of OR tasks. However, reliance on closed source LLM APIs raises data privacy concerns (Das et al., 2025), as sensitive problem descriptions and data often constitute commercial confidential information and must be transmit- 

- †Corresponding author. 

ted to proprietary platforms beyond the user’s control. Moreover, training open-source models from scratch incurs prohibitive computational costs (Xia et al., 2024). 

Fine-tuning pre-trained LLMs for domainspecific tasks offers a resource-efficient alternative, but vanilla LLMs struggle with precise arithmetic (McLeish et al., 2024). Tool-learning techniques enable LLMs to invoke external tools, such as calculators or specialized APIs, thereby combining generative flexibility with solver accuracy (Schick et al., 2023; Shi et al., 2025). We introduce OR-Toolformer<sup>1</sup> , which fine-tunes Llama3.1-8B-Instruct to extract structured solver parameters from natural-language OR problem descriptions and generate corresponding API calls, fully automating the modeling and solution phases. 



Figure 1: Overview of OR-Toolformer. 

## **2 The Methodology of OR-Toolformer** 

OR-Toolformer automates OR tasks through three integrated components (Figure 1): 

- **Problem–Answer Data Generation** , a semiautomated pipeline that synthesizes diverse 

- 1publicly available after finishing peer reviewing 

OR problem-answer pairs across problem types, industry contexts, and representation formats to ensure domain and expression diversity; 

- **LLM Fine-Tuning** , which adapts pre-trained LLMs to parse natural-language descriptions and extract structured solver parameters; 

- **Problem Solving with OR Solvers** , where the fine-tuned model issues API calls to external optimization solvers, uniting language comprehension with computational precision. 

### **2.1 Problem-Answer Data Generation** 

High-quality instruction tuning for robust generalization requires OR problem-answer pairs that capture both domain-specific variation and diverse linguistic expressions (Albalak et al., 2024). Given the scarcity of datasets that include detailed modeling steps and solver API calls (Huang et al., 2025a; Mostajabdaveh et al., 2025), we introduce a three-stage, semi-automated pipeline for largescale synthesis of OR problem-answer pairs. Figure 2 presents an example linear programming (LP) problem-answer instance, highlighting the input key information (left-top) and the generated problem-answer pair (right) along with the corresponding API call (left-bottom). 



Figure 2: Snippet of the generation process of an LP problem-answer pair. 

**Stage 1: Parameter sampling.** We randomly sample OR problem parameters from realistic 

ranges (e.g., positive unit consumption rates). These values are converted into structured API inputs and validated by the solvers. To ensure _domain diversity_ , we vary application contexts (e.g., agriculture, logistics, finance) and objective types (profit maximization, cost minimization). For _expression diversity_ , the parameter set of OR problem is rendered in free-form text, matrix notation, and tabular lists. 

**Stage 2: Prompt-based statement and answer synthesis.** We embed the key information (the sampled parameters and context as illustrated in topleft of Figure 2) into a problem generation prompt template that instructs Gemini 2.0 Flash to generate coherent OR problem statements. We then augment the same key information with API usage descriptions in answer generation prompt template that instructs Gemini 2.0 Flash to produce both the chain of thoughts and the corresponding API call (bottom-right of Figure 2). These two prompts are shown in Appendix A.1 and A.2 respectively. 

**Stage 3: Quality filtering and formatting.** To mitigate hallucinations (Huang et al., 2025b), we execute the generated API call (dotted box in the right-bottom of Figure 2) and compare its result against that of the sampled parameters based API call (left bottom of Figure 2). Only problemanswer pairs with matching results are retained. Finally, we cast validated instances into a dialogue format aligning with instruction-tuning best practices (Ouyang et al., 2022; Qin et al., 2024; Patil et al., 2024). System messages list one correct tool and three distractors, user messages present the problem, and assistant messages deliver the chain of thoughts plus API calls. 

### **2.2 LLM Fine-Tuning** 

We fine-tune _Llama-3.1-8B-Instruct_ (Grattafiori et al., 2024) on our synthesized dataset via instruction tuning. Let _D_ = _{_ ( _Qi, Ai_ ) _}_<sup>_N_</sup> _i_ =1<sup>denote</sup> the set of _N_ OR problem–answer pairs, where each prompt _Qi_ comprises a system message and a user message, and _Ai_ is the corresponding assistant message. The model’s prediction for _Qi_ is _A_ ˆ _i_ = LLM _θ_ ( _Qi_ ). We optimize the parameters _θ_ by minimizing the negative log-likelihood (crossentropy) loss: 



where _Pθ_ ( _Ai | Qi_ ) is the probability assigned by the LLM to the reference output _Ai_ . 

### **2.3 Problem Solving with OR Solvers** 

After generating an OR problem solution, we extract the embedded API call strings and parse them into structured invocations as depicted by the connected dotted boxes in the bottom of Figure 2. We execute these on two external OR services, NEOS Server<sup>2</sup> and Google Operations Research API<sup>3</sup> , to compute numerical solutions for each instance<sup>4</sup> . 

## **3 Experiments** 

### **3.1 Experimental Setup** 

**Data generation.** We synthesize two datasets: one for instruction fine-tuning and another to evaluate zero-shot generalization on unseen OR problem types. Table 1 details the number of instances per problem category. The fine-tuning dataset includes the same types of problems as those found in the four benchmarks including NL4OPT (Ramamonjison et al., 2023), MAMOEasyLP, MAMO-ComplexLP (Huang et al., 2024), and IndustryOR (Huang et al., 2025a). 

|||**Training**|**Datase**|**t**||
|---|---|---|---|---|---|
|LP|IP|MILP|TSP|MF|**Total**|
|3502|3501|3493|3516|3496|17508|
|||**Test D**|**ataset**|||
|TSP|MF|AP|MCF|||
|50|50|50|25||175|



**Abbreviations:** LP = Linear Programming; IP = Integer Programming; MILP = Mixed-Integer Linear Programming; TSP = Traveling Salesman Problem; MF = Maximum Flow; AP = Assignment Problem; MCF = Minimum-Cost Flow. 

Table 1: Summary statistics of training and test datasets. 

**Training.** We fine-tune _Llama-3.1-8B-Instruct_ on the full training set with a batch size of 64 and a learning rate of 2 _×_ 10<sup>_−_4</sup> . Using the Unsloth (Han and Han, 2023) framework on a single GPU (10 GB VRAM), we perform parameter-efficient finetuning via LoRA, 8-bit AdamW, and 4-bit quantization, updating only 0.52% of parameters. 

**Evaluation.** We measure execution accuracy following Huang et al. (Huang et al., 2025a), deeming a prediction correct if the solver’s returned optimum matches any ground-truth value. We benchmark OR-Toolformer against generalpurpose LLMs (ChatGPT, Gemini, DeepSeek- 

> 2https://neos-server.org/neos/ 

> 3https://developers.google.com/optimization/service 

> 4Google OR API is used to solve MF, MCF, and AP problems, as NEOS does not offer solvers for these problems. 

R1) and size-matched baselines: general LLMs (DeepSeek-7B, Mistral-7B, Qwen-2.5-7B) and math-focused LLMs (JiuZhang-3.0). 

### **3.2 Results Analysis** 

**Results on benchmarks.** Table 2 summarizes the execution accuracy of OR-Toolformer and baseline models on four standard benchmarks. All models achieve substantially higher accuracy on simpler tasks (NL4OPT, MAMO-EasyLP) than on more complex ones (MAMO-ComplexLP, IndustryOR). Consistent with scaling laws (Kaplan et al., 2020), larger general-purpose LLMs outperform their smaller counterparts on three of the four benchmarks. Accordingly, we focus our analysis on size-matched general-purpose and math-specific LLMs. Among 7-8 B models, OR-Toolformer delivers the highest accuracy across all benchmarks except IndustryOR, where it places second. In particular, OR-Toolformer attains 80.1% on MAMOEasyLP and approximately 14% on both MAMOComplexLP and IndustryOR, substantially outperforming other size-matched baselines, all of which fall below 18%. Although Qwen-2.5-7B-Instruct ranks second, math-specific LLMs generally outperform other size-matched models, underscoring the value of domain-specific fine-tuning (Zhang et al., 2024). 

**Results on the test dataset.** Table 3 compares OR-Toolformer and Qwen-2.5-7B-Instruct on two OR problem types (AP and MCF) not included in the benchmark suites. On two familiar problem types (TSP and MF), which were generated identically to our training data, OR-Toolformer achieves 100% and 98% execution accuracy, respectively, confirming the consistency of our synthesis pipeline. Crucially, on two entirely unseen problem types (AP and MCF), OR-Toolformer attains 68% and 40% accuracy versus 62% and 4% for Qwen-2.5-7B-Instruct, representing an average improvement of 21 percentage points. These results demonstrate OR-Toolformer’s strong zeroshot generalization to novel OR tasks. 

**Output token efficiency.** We evaluate the average output length of each model to assess token efficiency. OR-Toolformer generates concise responses, averaging 449 tokens, compared to 500 tokens for Qwen-2.5-7B-Instruct and 1,422 tokens for Qwen-2.5-Math-7B, the latter of which typically includes extensive mathematical derivations and embedded code. As illustrated in the bottomright of Figure 2, OR-Toolformer produces succinct 

||**Method**|**NL4OPT**|**MAMO-**<br>**EasyLP**|**MAMO-**<br>**ComplexLP**|**IndustryOR**|
|---|---|---|---|---|---|
||GPT-3.5|42.4%|61.8%|20.9%|19.0%|
|**Gl LLM**|GPT-4|47.3%|66.5%|14.6%|28.0%|
|**enera s**|Gemini-2.0 Flash|79.6%|77.3%|26.1%|23.0%|
||DeepSeek-R1-685B|66.1%|73.6%|48.3%|27.0%|
||DeepSeek-LLM-7B-Chat|5.7%|2.3%|0.5%|1.0%|
|**General LLMs**|Llama-3.1-8B-Instruct|6.9%|8.3%|7.6%|3.0%|
|**in similar scale**|Mistral-7B-Instruct-v0.3|0.0%|0.0%|0.0%|3.0%|
||Qwen-2.5-7B-Instruct|44.1%|43.6%|9.5%|**18.0%**|
||DeepSeek-Math-7B-Instruct|20.0%|30.7%|6.6%|10.0%|
|**Math LLMs**|DeepSeek-Math-7B-RL|23.7%|27.5%|10.4%|10.0%|
|<br>**in similar scale**|Qwen-2.5-Math-7B|40.8%|41.1%|10.9%|9.0%|
||JiuZhang-3.0-7B|13.9%|4.6%|3.3%|4.0%|
||JiuZhang-3.0-8B|23.7%|4.3%|4.3%|2.0%|
|**Ours**|OR-Toolformer-8B|**59.6%**|**80.1%**|**14.7%**|14.0%|



**Note.** The best results are in bold, and the second-best are underlined. Results in the first section are not included in the ranking. 

Table 2: Performance of OR-Toolformer and three types of baselines on four benchmarks. 

|Method|TSP|MF|AP|MCF|
|---|---|---|---|---|
|Qwen-2.5-7B-<br>Instruct|0.0%|16.0%|62.0%|4.0%|
|Ours|**100.0%**|**98.0%**|**68.0%**|**40.0%**|



Table 3: Performance of OR-Toolformer and Qwen-2.57B-Instruct on test dataset. 

natural-language outputs that satisfy both optimization and API-invocation requirements, thereby substantially reducing token consumption. 

## **4 Related Work** 

Tool learning enables LLMs to extend generative capacity by invoking external APIs. STE has models imagine, execute, and refine tool-usage sequences via simulated trial-and-error (Wang et al., 2024). Cooperative multi-agent methods decompose tool use into grounding, execution, and review stages (Shi et al., 2024), and budget-constrained planning generates cost-optimal call sequences under resource limits (Zheng et al., 2024). Selfinstruction pipelines synthesize diverse API-call examples from documentation (Yang et al., 2023), further scaled by Shi et al.(Shi et al., 2025). Largescale benchmarks such as StableToolBench(Guo et al., 2024) and RoTBench (Ye et al., 2024b) standardize evaluation, and ToolSword exposes safety vulnerabilities across tool-learning stages (Ye et al., 2024a). Unlike prior work focused on calculatorbased tools (Schick et al., 2023), our method emphasizes solver learning for OR, leveraging self- 

instruction generated training data (Yang et al., 2023). 

LLMs have been applied to automate OR task formulation and solution. The NL4OPT competition provides a widely used benchmark (Ramamonjison et al., 2023), and Mostajabdaveh et al.(Mostajabdaveh et al., 2025) evaluate opensource LLMs on complex OR problems. Chain-ofExperts and Optimus combine prompt engineering and multi-agent pipelines using GPT-4 for OR formulation (Xiao et al., 2023; AhmadiTeshnizi et al., 2024). LLMs have also been used to help interpret optimization results and identify infeasible optimization problems (Li et al., 2023; Chen et al., 2024). To mitigate privacy and computational costs, ORLM fine-tunes open-source models end-to-end for solver-code generation (Huang et al., 2025a). In contrast, we employ parameter-efficient fine-tuning to yield concise natural language formulations and structured API calls. 

## **5 Conclusion** 

We present OR-Toolformer, a fine-tuned Llama3.1-8B-Instruct model augmented with external OR solvers. It achieves 80.1% execution accuracy on three standard benchmarks, outperforming size-matched LLMs, and 54% average zero-shot accuracy on two novel problem types (a 21 pp improvement). These results confirm the efficacy of tool-augmented LLM fine-tuning for both accuracy and generalization in OR tasks. Future work will explore integrating agents via a model-context protocol. 

## **Limitations** 

Our study has several limitations. First, ORToolformer’s accuracy on complex or industryscale OR tasks (e.g., MAMO-ComplexLP, IndustryOR) remains substantially lower than on simpler academic benchmarks, which may impede realworld deployment. Second, due to computational constraints, we fine-tuned and evaluated only a single open-source LLM; a broader comparison across additional models is left to future work. Third, our synthetic data pipeline relies on heuristic prompt templates and limited domain context; incorporating stronger LLMs and richer industrial scenarios could enhance data realism and diversity. Finally, we have not yet conducted user-centered evaluations to measure the framework’s usability and utility in practical optimization workflows. 

## **References** 

- Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. 2024. Optimus: scalable optimization modeling with (mi) lp solvers and large language models. In _Proceedings of the 41st International Conference on Machine Learning_ , pages 577–596. 

- Alon Albalak, Yanai Elazar, Sang Michael Xie, Shayne Longpre, Nathan Lambert, Xinyi Wang, Niklas Muennighoff, Bairu Hou, Liangming Pan, Haewon Jeong, Colin Raffel, Shiyu Chang, Tatsunori Hashimoto, and William Yang Wang. 2024. A survey on data selection for language models. _Transactions on Machine Learning Research_ . Survey Certification. 

- Hao Chen, Gonzalo E Constante-Flores, and Can Li. 2024. Diagnosing infeasible optimization problems using large language models. _INFOR: Information Systems and Operational Research_ , 62(4):573–587. 

- Badhan Chandra Das, M Hadi Amini, and Yanzhao Wu. 2025. Security and privacy challenges of large language models: A survey. _ACM Computing Surveys_ , 57(6):1–39. 

- Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad AlDahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, and 1 others. 2024. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ . 

- Zhicheng Guo, Sijie Cheng, Hao Wang, Shihao Liang, Yujia Qin, Peng Li, Zhiyuan Liu, Maosong Sun, and Yang Liu. 2024. StableToolBench: Towards stable large-scale benchmarking on tool learning of large language models. In _Findings of the Association for Computational Linguistics: ACL 2024_ , pages 11143–11156, Bangkok, Thailand. Association for Computational Linguistics. 

Daniel Han and Michael Han. 2023. Unsloth. 

- Chenyu Huang, Zhengyang Tang, Shixi Hu, Ruoqing Jiang, Xin Zheng, Dongdong Ge, Benyou Wang, and Zizhuo Wang. 2025a. Orlm: A customizable framework in training large models for automated optimization modeling. _Operations Research_ . 

- Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and 1 others. 2025b. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _ACM Transactions on Information Systems_ , 43(2):1–55. 

- Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao, and Benyou Wang. 2024. Mamo: a mathematical modeling benchmark with solvers. _arXiv preprint arXiv:2405.13144_ . 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. 2020. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ . 

- Beibin Li, Konstantina Mellou, Bo Zhang, Jeevan Pathuri, and Ishai Menache. 2023. Large language models for supply chain optimization. _arXiv preprint arXiv:2307.03875_ . 

- Sean McLeish, Arpit Bansal, Alex Stein, Neel Jain, John Kirchenbauer, Brian Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Jonas Geiping, Avi Schwarzschild, and 1 others. 2024. Transformers can do arithmetic with the right embeddings. In _Advances in Neural Information Processing Systems_ , pages 108012– 108041. 

- Mahdi Mostajabdaveh, Timothy Tin Long Yu, Samarendra Chandan Bindu Dash, Rindra Ramamonjison, Jabo Serge Byusa, Giuseppe Carenini, Zirui Zhou, and Yong Zhang. 2025. Evaluating llm reasoning in the operations research domain with orqa. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 24902–24910. 

- Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, and 1 others. 2022. Training language models to follow instructions with human feedback. In _Advances in Neural Information Processing Systems_ , pages 27730–27744. 

- Shishir G Patil, Tianjun Zhang, Xin Wang, and Joseph E Gonzalez. 2024. Gorilla: Large language model connected with massive apis. In _Advances in Neural Information Processing Systems_ , pages 126544– 126565. 

- Fotios Petropoulos, Gilbert Laporte, Emel Aktas, Sibel A Alumur, Claudia Archetti, Hayriye Ayhan, Maria Battarra, Julia A Bennell, Jean-Marie Bourjolly, John E Boylan, and 1 others. 2024. Operational 

research: methods and applications. _Journal of the Operational Research Society_ , 75(3):423–617. 

- Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, dahai li, Zhiyuan Liu, and Maosong Sun. 2024. ToolLLM: Facilitating large language models to master 16000+ real-world APIs. In _The Twelfth International Conference on Learning Representations_ . 

- Rindranirina Ramamonjison, Timothy Yu, Raymond Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar, Shiqi He, Mahdi Mostajabdaveh, Amin BanitalebiDehkordi, Zirui Zhou, and 1 others. 2023. Nl4opt competition: Formulating optimization problems based on their natural language descriptions. In _Proceedings of the NeurIPS 2022 Competitions Track_ , pages 189–203. 

- Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, and 1 others. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995):468–475. 

- Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. 2023. Toolformer: Language models can teach themselves to use tools. In _Advances in Neural Information Processing Systems_ , volume 36, pages 68539–68551. 

- Zhengliang Shi, Shen Gao, Xiuyi Chen, Yue Feng, Lingyong Yan, Haibo Shi, Dawei Yin, Pengjie Ren, Suzan Verberne, and Zhaochun Ren. 2024. Learning to use tools via cooperative and interactive agents. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ , pages 10642–10657, Miami, Florida, USA. Association for Computational Linguistics. 

- Zhengliang Shi, Shen Gao, Lingyong Yan, Yue Feng, Xiuyi Chen, Zhumin Chen, Dawei Yin, Suzan Verberne, and Zhaochun Ren. 2025. Tool learning in the wild: Empowering language models as automatic tool agents. In _Proceedings of the ACM on Web Conference 2025_ , pages 2222–2237. 

   - Yuchen Xia, Jiho Kim, Yuhan Chen, Haojie Ye, Souvik Kundu, Cong Callie Hao, and Nishil Talati. 2024. Understanding the performance and estimating the cost of llm fine-tuning. In _2024 IEEE International Symposium on Workload Characterization_ , pages 210– 223. 

   - Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Jessica Wang, Xiongwei Han, Xiaojin Fu, Tao Zhong, Jia Zeng, Mingli Song, and 1 others. 2023. Chain-of-experts: When llms meet complex operations research problems. In _The twelfth international conference on learning representations_ . 

   - Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao Ge, Xiu Li, and Ying Shan. 2023. Gpt4tools: Teaching large language model to use tools via self-instruction. In _Advances in Neural Information Processing Systems_ , pages 71995–72007. 

   - Junjie Ye, Sixian Li, Guanyu Li, Caishuang Huang, Songyang Gao, Yilong Wu, Qi Zhang, Tao Gui, and Xuanjing Huang. 2024a. ToolSword: Unveiling safety issues of large language models in tool learning across three stages. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 2181– 2211, Bangkok, Thailand. Association for Computational Linguistics. 

   - Junjie Ye, Yilong Wu, Songyang Gao, Caishuang Huang, Sixian Li, Guanyu Li, Xiaoran Fan, Qi Zhang, Tao Gui, and Xuanjing Huang. 2024b. RoTBench: A multi-level benchmark for evaluating the robustness of large language models in tool learning. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 313–333, Miami, Florida, USA. Association for Computational Linguistics. 

   - Biao Zhang, Zhongtao Liu, Colin Cherry, and Orhan Firat. 2024. When scaling meets LLM finetuning: The effect of data, model and finetuning method. In _The Twelfth International Conference on Learning Representations_ . 

   - Yuanhang Zheng, Peng Li, Ming Yan, Ji Zhang, Fei Huang, and Yang Liu. 2024. Budget-constrained tool learning with planning. In _Findings of the Association for Computational Linguistics: ACL 2024_ , pages 9039–9052, Bangkok, Thailand. Association for Computational Linguistics. 

- Boshi Wang, Hao Fang, Jason Eisner, Benjamin Van Durme, and Yu Su. 2024. LLMs in the imaginarium: Tool learning through simulated trial and error. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 10583–10604, Bangkok, Thailand. Association for Computational Linguistics. 

- Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and Pengfei Liu. 2025. Evaluating mathematical reasoning beyond accuracy. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 27723–27730. 

## **A Question and Answer Generation Prompts** 

### **A.1 Problem Generation Prompt Template** 

Figure 3 shows the prompt template for generating linear programming problem statements, with key information of problems (as illustrated in Figure 2) inserted into {}. 





Figure 4: Answer generation prompt template. 

## **B Data, Code, and Model Availability** 

The dataset, source code, and model checkpoints are available at the anonymized URL for peer review: https://figshare.com/s/ 262251a08ea7f79113d7. 

Figure 3: Problem generation prompt template. 

### **A.2 Answer Generation Prompt Template** 

Figure 4 shows the prompt template for generating answers, with the API usage description and OR question statements (as illustrated in Figure 2) inserted into {}. This template is used to generate input for OR-Toolformer and all baselines. 

