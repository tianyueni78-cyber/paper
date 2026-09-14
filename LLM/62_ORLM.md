# ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling 

**Chenyu Huang**<sup>1∗</sup> **, Zhengyang Tang**<sup>2</sup><sup>_,_3∗</sup> **, Shixi Hu**<sup>5</sup> **, Ruoqing Jiang**<sup>6</sup> **Xin Zheng**<sup>7</sup> **, Dongdong Ge**<sup>4†</sup> **, Benyou Wang**<sup>2</sup><sup>_,_3</sup> **, Zizhuo Wang**<sup>2†</sup> 

> 1 Shanghai University of Finance and Economics 

> 2 The Chinese University of Hong Kong, Shenzhen (CUHK-Shenzhen) 

> 3 Shenzhen Research Institute of Big Data 

> 4 Shanghai Jiao Tong University 

> 5 Cardinal Operations 

> 6 Columbia University 

> 7 Duke University 

_chenyuhuang@stu.sufe.edu.cn zhengyangtang@link.cuhk.edu.cn shixi@shanshu.ai rj2556@columbia.edu xin.zheng@duke.edu ddge@sjtu.edu.cn {wangbenyou,wangzizhuo}@cuhk.edu.cn_ 

Optimization modeling plays a critical role in the application of Operations Research (OR) tools to address real-world problems, yet they pose challenges and require extensive expertise from OR experts. With the advent of large language models (LLMs), new opportunities have emerged to streamline and automate such task. However, current research predominantly relies on closed-source LLMs such as GPT-4, along with extensive prompt engineering techniques. This reliance stems from the scarcity of high-quality training datasets for optimization modeling, resulting in elevated costs, prolonged processing times, and privacy concerns. To address these challenges, our work is the first to propose a viable path for training open-source LLMs that are capable of optimization modeling and developing solver codes, eventually leading to a superior ability for automating optimization modeling and solving. Particularly, we design the OR-Instruct, a semi-automated data synthesis framework for optimization modeling that enables customizable enhancements for specific scenarios or model types. This work also introduces IndustryOR, the first industrial benchmark for evaluating LLMs in solving practical OR problems. We train several 7B-scale open-source LLMs using synthesized data (dubbed ORLMs), which exhibit significantly enhanced optimization modeling capabilities, achieving competitive performance across the NL4OPT, MAMO, and IndustryOR benchmarks. Additionally, our experiments highlight the potential of scaling law and reinforcement learning to further enhance the performance of ORLMs. The workflows and human-machine interaction paradigms of ORLMs in practical industrial applications are also discussed in the paper. 

_Key words_ : Automated optimization modeling, large language model, synthetic data 

### **1. Introduction** 

Optimization models have been a critical analytical tool for business decision-making, aiding companies in making optimal choices under various complex decision environments. With the fast 

> 1 _∗_ These authors contributed equally to this work. 

> 2 _†_ Corresponding author. 

1 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

2 

development of computing capability (including both the development of algorithm and hardware) and the growing amount of data, optimization models are playing more and more significant roles in the operations of large corporations. For instance, optimization techniques used by JD.com enable them to handle 10 times the normal volume of orders during peak sales seasons, helping the company decrease its fulfillment expense ratio to a world-leading level of 6.5%, which has resulted in hundreds of millions of dollars in savings (Qin et al. 2022). Baosteel, one of the largest steel company in China, utilized integer optimization for production planning at its main plant in Shanghai, leading to a significant reduction in carbon monoxide emissions — over 500,000 tons annually — as reported by INFORMS (2013). The U.S. Census Bureau was recognized as a finalist for the 2022 Franz Edelman Award for their innovative use of operations research and analytics in reengineering field operations for the 2020 U.S. Census. This project utilizes advanced analytics, optimization, and machine learning techniques to automate and optimize the scheduling, workload assignments, and management of field data collection, a process previously done manually (Adams et al. 2023). Despite the huge amount of success stories, the sensitivity of optimization models to environmental changes necessitates frequent adjustments in dynamically evolving business contexts. This, combined with the high level of expertise and substantial labor costs required for optimization modeling, represents a significant bottleneck that has hindered the full potential to be unlocked for optimization techniques. 

The advent of large language models (LLMs) gives an emerging hope to the above challenge. As soon as its advent, these pre-trained LLMs have exhibited remarkable capabilities in rapid knowledge comprehension and cross-disciplinary learning, demonstrating remarkable success and transformative potential across various fields (Huang et al. 2024a), like medical consultation (Wang et al. 2023b), software development (Zaremba et al. 2021), offering stock market trading strategies (Chen et al. 2022b), improving recommendation systems (Xu et al. 2024), and enhancing marketing research (Wang et al. 2024). In the realm of more abstract mathematical reasoning, research has increasingly incorporated more techniques to enhance the capabilities of large models, yielding promising results. For example, Trinh et al. (2024) train Alphaproof with hundreds of billions of synthetic data used to tackle complex olympiad geometry problems. Similarly, MathScale (Tang et al. 2024) offers a straightforward and scalable method to generate high-quality data for mathematical reasoning, establishing a foundation for further training of large language models in mathematical reasoning capabilities. 

In recent years, with the advancements in pre-trained language models (PLMs) such as GPT-4 and Claude-3.5, a growing number of studies have explored automating the modeling and solving of optimization problems expressed in natural language. To produce complete solutions, including executable programs that leverage established solvers, existing approaches often employ prompt engineering techniques and multi-agent collaboration frameworks built on proprietary LLMs, such as 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

3 

Chain-of-Experts (Xiao et al. 2023), OptiMUS (AhmadiTeshnizi et al. 2024), and OptiGuide (Li et al. 2023a). However, utilizing online APIs for advanced large models offers no assurances of privacy protection, which is prohibitive in some sensitive industry applications. Additionally, these approaches are heavily reliant on the inherent capabilities of the foundational LLMs themselves, rendering them incapable of addressing the customized needs of users. As illustrated in Figure 1, even a basic optimization modeling problem presents challenges for the cutting-edge foundational large language model, GPT-4. It demonstrates deficiencies in comprehending and transforming logical constraints, which imposes a limitation on methods dependent on these general closed-source LLMs. 



<!-- Start of picture text -->
Toy manufacturers can produce and sell toy trucks, airplanes, boats, and trains. The profit from selling  User<br>one truck is $5, one airplane is $10, one boat is $8, and one train is $7. During the production process,<br>890 units of wood are available. Manufacturing one truck requires 12 units of wood, one airplane requires<br>20 units of wood, one boat requires 15 units of wood, and one train requires 10 units of wood. There are<br>500 units of steel available. Manufacturing one airplane requires 3 units of steel, one boat requires 5 units<br>of steel, one train requires 4 units of steel, and one truck requires 6 units of steel.<br>In actual production operations, the following production conditions must be observed:<br>1. If trucks are manufactured, trains will not be manufactured.<br>2. If boats are manufactured, airplanes will also be manufactured.<br>3. The number of toy boats manufactured cannot exceed the number of toy trains manufactured. Logic constraints<br>How many types of toys should the manufacturer produce to maximize profit?<br>Mathematical Model:<br>GPT-4 To solve this problem, we can formulate it as a linear programming problem. We will define the decision<br>variables, objective function, and constraints, then use a solver to find the optimal solution.<br>Decision Variables:<br>▪ 𝑥1: Number of toy trucks produced.<br>▪ 𝑥2: Number of toy airplanes produced.<br>▪ 𝑥3: Number of toy boats produced.<br>▪ 𝑥4: be the number of toy trains produced.<br>Objective Function:<br>▪ Maximize profit: Profit = 5𝑥1 + 10𝑥2 + 8𝑥3 + 7𝑥4<br>Constraints:<br>1. Wood constraint: 12𝑥1 + 20𝑥2 + 15𝑥3 + 10𝑥4 ≤890<br>2. Steel constraint: 6𝑥1 + 3𝑥2 + 5𝑥3 + 4𝑥4 ≤500<br>3. If trucks are manufactured, trains will not be manufactured: 𝑥1 ⋅𝑥4 = 0<br>4. If boats are manufactured, airplanes will also be manufactured: 𝑥3 ≤𝑥2<br>5. The number of toy boats manufactured cannot exceed the number of toy trains manufactured: 𝑥3 ≤𝑥4<br>6. Non-negativity constraints: 𝑥1, 𝑥2, 𝑥3, 𝑥4 ≥0<br><!-- End of picture text -->

**Figure 1** An example is presented to illustrate the failure of advanced large models to accurately respond to seemingly straightforward optimization modeling questions. The responses highlighted in reds contain errors, specifically the introduction of non-linear terms and misunderstandings of logical relationships. This response was generated in June 2024, originating from the web-based GPT-4. 

In summary, existing large language models (LLMs) for optimization modeling exhibit the following deficiencies: 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

4 

1. **Limited modeling capabilities.** Contemporary advanced LLMs frequently exhibit errors in interpreting logical constraints or inadvertently incorporate nonlinear elements, making it difficult to model real-world problems effectively. 

2. **Insufficient quality of optimization modeling training data.** The quality and scale of data are directly proportional to the capability of the model, as described by the _Scaling Law_ (Kaplan et al. 2020). However, a shortage in high-quality optimization modeling training data is often a critical challenge, obstructing the advancement of LLMs’ modeling ability. 

3. **Data privacy concerns.** Dependence on APIs for closed-source LLMs may lead to data breaches which hampers the broader adoption and development of LLM technologies in the industrial sector. 

4. **Test sets are relatively homogeneous.** The efficacy of large language models in automatic modeling is predominantly assessed using the dataset provided by the NL4OPT competition (Ramamonjison et al. 2023). This dataset primarily focuses on simple linear programming tasks that exhibit relatively low complexity, narrow scope, and few types compared to real-world applications. 

To fill this gap, this paper introduces, for the first time, a new path for training an open-source large language model specifically designed for modeling and solving optimization problems. To address the core of the above challenges, we present a semi-automated framework for the synthesis of high-quality optimization modeling data, aimed at progressively enhancing the specialized modeling capabilities of LLMs. We hope that this approach will inspire future research and serve as a foundation for the deeper integration of large models with operations research. Our main contributions can be summarized as follows: 

1. To ensure the effectiveness, robustness, and real-world applicability of our model, we have identified four crucial requirements that the training dataset must fulfill, as informed by academic research like Alzubaidi et al. (2023), Jiang et al. (2024) and industry insights. Inspired by these requirements, we design and implement OR-Instruct, a semi-automated process for creating synthetic data tailored to optimization modeling. The process uses an iterative bootstrapping algorithm (see Figure 2). Initially, we collect a set of seed industry cases (e.g., 686 cases in our study) and add them to the training data pool. Following this, we use two strategies. One is expansion, which employs GPT-4 and leverages its in-context learning capability to generate data spanning diverse scenarios and question types. Another is the augmentation strategy, which involves modifying objectives and constraints, rephrasing questions, and incorporating diverse modeling techniques to ensure the difficulty and quality of generation problems. Finally, heuristics are used to automatically filter out obviously low-quality data. This cycle can be repeated multiple iterations until the training data pool reaches the requisite volume (e.g., 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

5 

- 32,481 cases in our study). Notably, this approach is highly customizable; new seed data and scenarios can be seamlessly introduced to adapt the dataset to specific needs. 



<!-- Start of picture text -->
Scenario Question Model Code<br>Expansion<br>Training Data Pool Filtering<br>Seed Data<br>Altering Rephasing Incorporating<br>Obj&Constraints Questions Multiple Techniques<br>Augmentation<br>Training LLMs<br><!-- End of picture text -->

**Figure 2** Overview of OR-Instruct. 

2. To evaluate the efficacy of OR-Instruct, we introduce IndustryOR, the inaugural industrial benchmark tailored for optimization modeling. This benchmark uses data sourced from 13 different industries, covering 5 types of questions across 3 levels of difficulty. For comprehensive evaluation, we also include NL4OPT (Ramamonjison et al. 2023) and MAMO (Huang et al. 2024b) benchmarks. 

3. We utilize the synthetic data generated by OR-Instruct to train a series of open-source large language models, each approximately 7 billion parameters in size, including Mistral-7B (Jiang et al. 2023), Deepseek-Math-7B-Base (Shao et al. 2024), and LLaMA-3-8B (AI@Meta 2024). We designate these trained models as Operation Research Language Models (ORLMs) and observe a marked enhancement in their optimization modeling capabilities. Our experimental results show that the best-performing ORLM achieves competitive performance on the NL4OPT, MAMO, and IndustryOR benchmarks. Building upon this foundation, we conduct extensive numerical experiments to analyze the limitations of the ORLM and propose feasible solutions for its improvement. The results highlight the promising prospects of ORLM in advancing the application and development of operations research, while also suggesting potential humanLLM collaboration frameworks. These frameworks demonstrate how ORLM could enhance the productivity of both industry and academia in the field of operations research. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

6 

To our best knowledge, this work is the first initiative to train open-source LLMs specifically for optimization modeling in real-world industries. The proposed approach significantly reduces the reliance on closed-source LLMs thus adding significant flexibility to the training process and greatly enhancing privacy preservation for industrial applications. Remarkably, the highest-performing ORLM achieves competitive results on the NL4OPT, MAMO, and IndustryOR benchmarks. This suggests that in the field of optimization modeling, our approach enables ORLMs with approximately 7 billion parameters to outperform many cutting-edge large language models, such as GPT-4, Llama-3.1, Qwen 2.5, and related agent-based frameworks. 

We also conduct a thorough analysis of the ORLM’s results, with numerous ablation experiments validating the effectiveness of our approach. The results show that, although ORLM performs relatively weak on some challenging datasets, several strategies can still ensure improvements in its performance. For instance, applying scaling laws to further increase the model size and data scale leads to continuous performance enhancements. Additionally, we find that ORLM has weak ranking capabilities for optimal optimization models. Using alignment strategies, such as reinforcement learning, also helps strengthen ORLM’s performance. 

Furthermore, we want to comment that the proposed data synthesis method, the _OR-Instruct_ , has the ability to facilitate customization to address particular needs of larger models, such as supply chain management, scheduling, inventory issues, or enhancing capabilities in linear programming, integer programming, and mixed integer programming. This synthetic data framework robustly addresses the scarcity of training data for optimization modeling, provides a valuable reference for advancing the application of operations research in various industrial sectors with the support of large models. In Section 6.1, we provide a detailed discussion of representative workflows driven by large models. 

Finally, we note that almost all of our results, including certain samples from the training data set, industry-level benchmark for optimization modeling, and all the best-performing LLMs that have been fine-tuned, are made open source. We hope that our work can serve as a foundation for subsequent explorations, empowering future researchers to enhance the utility and efficiency of large language models in optimization modeling. 

The structure of this paper is organized as follows: Section 2 reviews the literature related to our research. Section 3 delineates four essential conditions required for the training data and outlines the implementation specifics of the semi-automated synthetic data framework for optimized modeling, OR-Instruct. Section 4 examines the impact of training open-source large models on various test sets and presents the experimental outcomes of customized enhancements in modeling capabilities. Section 5 analyzes the limitations of ORLM through extensive experiments and discusses potential areas for improvement. Section 6 discusses the practical application scenarios of ORLM and explores 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

7 

future research directions based on the conclusions drawn in this paper. We conclude the paper in Section 7. 

### **2. Literature Review** 

Our research is related to several streams of literature, we will provide a detailed review of each stream below. 

**AI approach for facilitating solution to operations research problems.** With the fast development of AI techniques, there have been a growing amount of research leveraging advanced techniques, such as deep learning, to address challenging operational research (OR) problems traditionally resistant to conventional methods. For example, in the supply chain context, Gijsbrechts et al. (2022) employ deep reinforcement learning to enhance inventory management, demonstrating parity with leading heuristics and approximate dynamic programming approaches. Qi et al. (2023) investigate a data-driven multi-period inventory replenishment problem with uncertain demand and vendor lead time, propose a one-step end-to-end framework that uses deep learning models to output the suggested replenishment amount directly from input features. In the revenue management field, Aouad and Désir (2022) propose a neural network-based discrete choice model called RUMnets, which combines the theoretical robustness of traditional economic models with the flexibility and learning capabilities of modern artificial intelligence approaches, leading to better predictions and insights into consumer behavior. Wang et al. (2023a) explore the deployment of deep neural networks in making the optimal assortment selection, demonstrating its effectiveness in capturing consumer choice. As for queuing theory, Dai and Gluzman (2022) investigate the deployment of advanced policy gradient methods for controlling multi-class queueing networks, underscoring the superior efficacy of the PPO algorithm under diverse load scenarios. For personalized recommendation, Wang et al. (2023c) utilize a novel unsupervised deep learning network and graph embedding techniques to improve recommendation accuracy and diversity by effectively transferring check-in patterns across different geographical contexts. Regarding general Markov decision process, Zhang et al. (2021) introduce a model-free reinforcement learning algorithm that attains asymptotically optimal sample complexity for learning an _ϵ_ -optimal policy within discounted Markov decision processes (MDPs). In addition, these techniques have been used in demand prediction, for example, Lee et al. (2024) propose a Transformer-based methodology for time series conformal prediction, utilizing its decoder to estimate prediction intervals through the quantile prediction of residuals, showcasing enhanced performance over existing conformal prediction techniques. Chen et al. (2020) introduce a novel architecture of convolutional neural networks (CNNs) that significantly improves forecasting by 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

8 

modeling the conditional distribution of future series data directly, rather than relying on traditional autoregressive methods. 

AI technology also demonstrates significant strengths in facilitating the implementation of operations research, for instance, Liu et al. (2023) employ reinforcement learning combined with spatial data to optimize the allocation of resources and strategize for disease outbreak responses. Parmentier (2022) introduces a novel paradigm that integrates machine learning with operations research to efficiently approximate complex industrial problems by transforming them into classic, more tractable optimization challenges. 

In addition, there have also been recent attempts in using AI methods to empower optimization algorithm design. For instance, deep learning or machine learning can be used to accelerate conventional optimization algorithms for tackling mixed-integer programming problems (e.g., Chen et al. 2023c, Nair et al. 2020). Numerous researchers also explore end-to-end optimization problem-solving strategies based on deep learning methods, motivated by the high structural similarity among many optimization problems, with differences primarily in data distribution (e.g., Chen et al. 2022a, Khalil et al. 2017). Compared to this work, the above stream of works studies the integration of AI approach and traditional OR approaches in solving OR problems. In contrast, the main focus of the present work is in the facilitation and automation of the modeling process of the optimization model, which is different from the above stream. 

**Automated optimization modeling** is an emerging area, which aims to automate mathematical modeling and solving tasks to facilitate efficient decision-making. Recently, a growing body of studies have emerged, aiming to bridge the gap between natural language processing and mathematical optimization. One of the pioneering endeavors in this field is the NL4OPT competition, which focuses on formulating mathematical models for optimization problems (Ramamonjison et al. 2023). In particular, their work introduces a two-step framework using PLMs and offers a widely used benchmark for intelligence mathematical modeling. Expanding on this, Xiao et al. (2023) introduce Chain-of-Experts, a multi-agent LLM framework to build optimization model that significantly outperforms GPT-4 by incorporating domain-specific knowledge and cooperative reasoning strategies. AhmadiTeshnizi et al. (2024) propose OptiMUS, a robust LLM-based agent designed to formulate and solve MILP problems. This system not only develops mathematical models but also assists in writing and debugging solver code, showcasing a comprehensive solution that extends beyond simple problem formulation. Similarly, Li et al. (2023a) develop a framework called OptiGuide which leverages LLMs to interpret and explain optimization outcomes in supply chain management, thereby enhancing stakeholder comprehension and trust. In terms of diagnosing and resolving optimization issues, Chen et al. (2023a) introduce OptiChat, a natural language-based system equipped with 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

9 

GPT-4, which assists in identifying and addressing infeasible optimization models. Unlike these methods, our approach involves fine-tuning open-source LLMs and delivering a complete solution using direct prompting, which is more concise and privacy-preserving than multi-agents interaction and simply calling API from advanced LLMs like GPT-4. 

**Synthetic data** plays a crucial role in enhancing the capabilities of large language models by providing controlled, high-quality datasets that help fill gaps in real-world data, eliminate biases, and improve model robustness. A review of literature on synthetic data and LLMs is referred to Ding et al. (2024). In the field of synthetic data for optimization modeling, traditional methods often require specialized knowledge to convert real-world problems into mathematical models, which limits their accessibility and flexibility. Most research focuses on how to automatically generate mixed-integer linear programming (MILP) models to overcome these challenges more effectively. For example, the methods proposed by Pawlak and Krawiec (2017) and Sroka and Pawlak (2018) utilize MILP examples for the synthesis of constraints. These methods develop an approach that can generate constraints from examples of both feasible and infeasible solutions, thereby demonstrating the feasibility of automating this conversion process. Further expanding on this theme, Pawlak and O’Neill (2021) leverage evolutionary strategies to generate constraints that improve the adaptability and efficiency of optimization models, thus enhancing the model’s flexibility in handling complex scenarios. Prasath and Karande (2023) examine the effectiveness of synthesizing mathematical programs from natural language specifications based on NL4OPT competition dataset, focusing on data synthesis methods using the CodeT5 model with enhancements from data augmentation and post-processing. The study highlights how synthetic data generation, notably through techniques like reverse translation and parameter variation, significantly improves model performance in solving optimization problems. The synthetic data framework proposed in Li et al. (2023b) leverages LLMs to identify decision variables, classify constraints, and generate MILP models based on NL4OPT problems. This approach significantly outperforms traditional methods, achieving higher accuracy in constraint recognition and model formulation. In contrast to the aforementioned synthetic data approaches, the method proposed in this paper is designed for the general purpose of synthesizing high quality data for optimization modeling from unstructured natural language descriptions. This allows for the development of synthesis strategies that are not only tailored to specific problem but also capable of customized data augmentation. 

### **3. Semi-Automated Framework for Data Generation** 

In this section, we present the formal definition of the optimization modeling task. We first discuss some critical requirements for effectively training an open-source LLM to perform this task. Based 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

10 

on these requirements, we design a semi-automated data synthesis framework OR-Instruct which achieves the desired properties. 

#### **3.1. Data Requirements** 

Given an OR problem _p_ described in natural language, optimization modeling (Berry and Houston 1995, AhmadiTeshnizi et al. 2024) involves constructing a mathematical model _m_ that converts the real-world problem into an optimization model with concrete decision variables, objective function and constraints. Then, for large-scale problems, in order to obtain an optimal solution, we further need to convert the mathematical model into a program _c_ compatible with a specific optimization solver. Hence, an expected training example for this task is usually required in the form of the triplet ( _p,m,c_ ), as illustrated in Figure 3. Training a large language model _f_ for this task essentially involves learning a function _f_ : _p →_ ( _m,c_ ) that maps problems to their corresponding mathematical models and solver programs. In this paper, without loss of generality, COPT is employed as the default solver. COPT (Ge et al. 2022), an acronym for Cardinal Optimizer, is able to tackle large-scale optimization problems and achieves good performance in a variety of tasks (Hans 2002). We select the COPT solver because the predominant large language models available in the market have not yet mastered the COPT syntax. This choice underscores the efficiency and extensibility of our framework. However, any well-established solver may be utilized in the training dataset construction. 

In addition to the desired format as described above, a desired training dataset should demonstrate effectiveness, robustness, and practical applicability to real-world scenarios. In particular, 

Requirement 1. **Comprehensive Coverage:** The dataset should cover: 1) diverse scenarios such as supply chain optimization, scheduling, inventory management, and transportation logistics; 2) different problem types like linear programming, integer programming, and mixed integer programming; and 3) varying difficulty levels (easy, medium, hard) — we provide a way to describe the difficulty level of a problem in Appendix A.1. 

Requirement 2. **Environmental Adaptability:** In real-world industrial settings, the objectives and constraints of problems often change due to shifts in business goals, market conditions, or resource availability. A good optimization model should be able to adapt to those changes easily. Therefore, it is vital that the dataset includes cases reflecting these dynamic changes. 

Requirement 3. **Linguistic Diversity** : Problems described in natural language often show different syntax, ambiguities, and complexities. For example, one problem might mention "inventory overflow" while another refers to "excess stock". Including this Linguistic Diversity in the dataset could improve the model’s ability to understand varied descriptions. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

11 

##### **An Expected Training Example** 

##### **Input - Natural Language Problem:** 

- A company has three transportation options to choose from to transport 25 tons of cargo, namely trucks, airplanes, and ships with costs $100 _,_ $120 _,_ $130 per ton and capacities of 10 _,_ 20 _,_ 30 tons respectively. The company can’t choose trucks and ships together. How should the company optimize the selection and allocation of these methods to minimize overall costs? 

##### **Target - Mathematical Model and Program:** 



<!-- Start of picture text -->
## Mathematical Model:<br>### Variables:<br>- x 1 ,x 2 ,x 3: 0-1 variables indicating whether trucks, airplanes, and ships are selected, respectively.<br>- y 1 ,y 2 ,y 3: Non-negative continuous variables indicating the volume of cargo transported by three modes.<br>### Objectives and Constraints:<br>Minimize xi∈{ 0 , 1 },yi≥ 0 100 y 1 + 120 y 2 + 80 y 3<br>subject to<br>x 1 +  x 2 +  x 3  ≥ 1 (At least one transportation)<br>y 1  ≤ 10 x 1 , y 2  ≤ 20 x 2 , y 3  ≤ 30 x 3 (Capacity limits)<br>x 1 +  x 3  ≤ 1 (Mutual exclusion constraint)<br>y 1 +  y 2 +  y 3  ≥ 25 (Transportation requirements)<br>## Program using COPT solver:<br><!-- End of picture text -->



<!-- Start of picture text -->
1 import coptpy as cp<br>2 from coptpy import COPT<br>3 # Initialize the optimization environment<br>4 env = cp.Envr()<br>5 model = env.createModel("TransportationOptimization")<br>6 # Define costs and capacities for each mode of transportation<br>7 costs = {’trucks’: 100, ’airplanes’: 120, ’ships’: 130}<br>8 capacities = {’trucks’: 10, ’airplanes’: 20, ’ships’: 30}<br>9 # Define binary and continuous variables for each transportation mode<br>10 x = {mode: model.addVar(vtype=COPT.BINARY, name=f"x_{mode}") for mode in costs}<br>11 y = {mode: model.addVar(vtype=COPT.CONTINUOUS, lb=0, name=f"y_{mode}") for mode in costs}<br>12 # Set the objective function to minimize the total transportation cost<br>13 model.setObjective(sum(costs[mode] * y[mode] for mode in costs), sense=COPT.MINIMIZE)<br>14 # Add constraints<br>15 model.addConstr(x[’trucks’] + x[’airplanes’] + x[’ships’] >= 1, name="AtLeastOneMode")<br>16 for mode in costs:<br>17 model.addConstr(y[mode] <= capacities[mode] * x[mode], name=f"Capacity_{mode}")<br>18 model.addConstr(x[’trucks’] + x[’ships’] <= 1, name="ModeExclusivity")<br>19 model.addConstr(sum(y[mode] for mode in capacities) >= 25, name="Volume Requirement")<br>20 # Solve the model<br>21 model.solve()<br>22 # Check the solution status and print the optimal values of the variables<br>23 if model.status == COPT.OPTIMAL:<br>24 print("Optimal solution found:")<br>25 for mode in costs:<br>26 print(f"{mode}: x = {x[mode].x}, y = {y[mode].x}")<br><!-- End of picture text -->

**Figure 3** An expected training example for optimization modeling task. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

12 

Requirement 4. **Technique Variability:** For some challenging problems, there may be multiple modeling techniques, such as linearizing a nonlinear problem by introducing auxiliary variables, or introducing the big _M_ term in an integer optimization formulation. Including this variety in the dataset allows the model to learn different modeling techniques and approaches. 

#### **3.2.** OR-Instruct **: Towards Training Effective OR LLMs** 

In the above section, we describe some critical requirements on the dataset for an effective training of an LLM to be equipped with good optimization modeling capabilities. However, collecting data on a large scale that aligns with the above requirements presents significant challenges because: (1) such data primarily resides within private industrial cases, and no public datasets sufficiently meet the requirements, (2) training data suitable for optimization modeling is limited and requires extensive time to collect, and (3) conventional synthesis methods (for example, Wang et al. 2022) encounter substantial obstacles in generating this type of data, as will be elaborated below. In the following, to address the above challenges, we design and implement OR-Instruct, a semi-automated process for creating synthetic data tailored to these requirements. The overall pipeline of OR-Instruct is depicted in Figure 2, which iteratively applies two strategies, namely expansion and augmentation, to the training data pool, followed by the filtering of obviously low-quality data. 

**Initial Dataset** The quality of initial data plays a crucial role in large model training, providing a strong foundation for diversity and difficulty as a starting point (Marion et al. 2023). Additionally, in this customizable framework designed to enhance modeling capabilities, the category or domain of the optimization problem associated with the initial data is important. We will demonstrate later that when the initial dataset is concentrated in a specific type (e.g., scenario or type), it substantially enhances the LLM’s ability to model effectively within that domain. 

In our particular case, we start with 686 real-world industry cases collected from some OR textbooks and our previous industrial projects (after proper abstraction and anonymization). 

**Strategy 1: Expansion for Comprehensive Coverage.** Initially, OR-Instruct seeks to generate new data by expanding scenarios and question types from the training dataset using a bootstrapping approach powered by GPT-4. The process begins with GPT-4 generating a list of 100 scenarios where optimization models are applied in real-life contexts. In each iteration, three examples are selected from data pool to serve as in-context references for GPT-4, and one scenario is randomly chosen from the list. Among the three examples, two are sourced from real-world data, while the third, if available, is taken from data previously generated by the model. Finally, GPT-4 is prompted to create a new sample based on the three examples within the context of the selected scenario. This iterative approach promotes greater diversity in the resulting dataset. The prompting template for this expansion process is detailed in Appendix A.2. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

13 

It’s important to note that optimization models are naturally abstract, often built on similar logical ideas across various scenarios. In this setting, _Comprehensive Coverage_ not only exposes the LLMs to a broad range of situations but also helps it better grasp the underlying patterns and principles when modeling across these different contexts. However, it falls short of meeting the other requirements, especially concerning varying levels of difficulty. In manually reviewing the difficulty of generated example, of 50 cases, 87% are deemed easy, 13% medium, and none hard, as judged by criteria in Appendix A.1. We also provide examples in Appendix A.7 for comparing generated easy entries with real-world hard entries. Fortunately, the original seed data already shows a diverse range of difficulties. Thus, we can naturally enhance the difficulty diversity by augmenting them described in the next strategy, thereby further addressing _Comprehensive Coverage_ . 

**Strategy 2: Augmentation for Problem-Solution Diversity.** To fulfill the remaining requirements, the OR-Instruct adopts an augmentation strategy for the original seed data, designed to both enhance the diversity and robustness of the dataset while preserving the complexity inherent in optimization modeling problems. This strategy is crafted to mirror potential scenarios that might be encountered in real-world industrial applications, encompassing modifications such as alterations in problem descriptions, model adjustments, or concurrent changes. To address these three scenarios, the implementation of this strategy involves three specific tactics: rephrasing questions, modifying objectives and constraints, and integrating diverse modeling techniques. Together, these tactics aim to broaden the range of problem-solution diversity, thereby enriching the training dataset. 

- (a) **Altering Objectives and Constraints:** The first augmentation involves adding, removing, or replacing objectives and constraints in the problem, along with making necessary adjustments to the mathematical models and programs. Specifically, we start by providing GPT-4 with the original example and ask it to list five potential changes to the objectives and constraints. These suggested changes are then fed back to GPT-4 using a prepared few-shot prompt to modify the problem, model, and programs accordingly. This augmentation is designed to enhance _Environmental Adaptability_ . An example is provided in Figure 4, and the corresponding prompting template is shown in Appendix A.3.1. 

Remark 1. One important point to note is that during the process of altering objectives and constraints, GPT-4 may generate background scenarios that are illogical, such as presenting two contradictory constraints. However, this issue arises from unreasonable problem descriptions. As long as the model can accurately map each statement of the problem to the correct objectives and constraints, it can still yield the desired results when tested on meticulously designed datasets that reflect such issues. 

14 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

##### **Altering Objectives and Constraints for Requirement 2** 

##### **Original:** 

Q: ... The company can’t choose trucks and ships together. Denote the cost ... 

##### **Augmented:** 

- Q: ... The company can’t choose trucks and ships together. _Due to the special nature of the goods, the company has decided that if trucks are chosen, airplanes must also be selected for transportation._ Denote the cost ... 

A: ... _New dependency constraint (choosing trucks necessitates choosing airplanes): x_ 1 _≤ x_ 2 ... 



<!-- Start of picture text -->
1 ...<br>2 model.addConstr(x[’trucks’] <= x[’airplanes’], name="New constraint")<br>3 ...<br><!-- End of picture text -->

**Figure 4** An example illustrating altering objectives and constraints. _Italicized text_ denotes altered content. 

- (b) **Rephrasing Questions:** The second augmentation involves modifying the problem description while essentially addressing the same optimization model. This approach enhances the robustness of large language models (LLMs) to different prompts, enabling them to abstract a unified optimization model across various problem descriptions. This process involves instructing GPT-4 to rewrite the target problem, either simplifying or complicating it, while ensuring the core logic aligns with the solution, including the mathematical model and programs. This augmentation is designed to enhance _Linguistic Diversity_ . An example is provided in Figure 5, and the corresponding prompting template is shown in Appendix A.3.2. 

##### **Rephrasing Questions for Requirement 3** 

##### **Original:** 

Q: A company has three transportation options to choose from to transport 25 tons of cargo, namely trucks, airplanes, and ships with costs $100 _,_ $120 _,_ $130 per ton and capacities of 10 _,_ 20 _,_ 30 tons respectively. The company can’t choose trucks and ships together. How should the company optimize the selection and allocation of these methods to minimize overall costs? 

##### **Augmented:** 

Q: _A corporation wants to transport 25 tons of cargo with least cost, and must choose from three transportation modes: trucks, airplanes, and ships. These options cost $100, $120, and $130 per ton, respectively, with capacities of 10, 20, and 30 tons. However, trucks and ships cannot be used together._ 

**Figure 5** An example illustrating rephrasing questions. _Italicized text_ denotes the question that has been rephrased. 

- (c) **Incorporating Multiple Modeling Techniques:** The third augmentation explores the use of different modeling techniques. We identify five potential techniques from engineers’ experiences, such as introducing auxiliary variables or using the Big _M_ method, for GPT-4 to choose from 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

15 

in modifying an objective or constraint in the original mathematical model. This augmentation is designed to enhance _Solution Variability_ . An example is provided in Figure 6, and the corresponding prompting template is shown in Appendix A.3.3. 



<!-- Start of picture text -->
Incorporating Multiple Modeling Techniques for Requirement 4<br><!-- End of picture text -->



<!-- Start of picture text -->
Original:<br>A: Mutual exclusion constraint (trucks and ships cannot be selected simultaneously): x 1 +  x 3  ≤ 1<br>Augmented:<br>A: Mutual exclusion constraint (Using big M method): x 1  ≤ (1  − x 3) M, where M is a large number<br>1 ...<br>2 model.addConstr(x[’trucks’] <= (1-x[’ships’])*M, name="New constraint")<br>3 ...<br><!-- End of picture text -->

**Figure 6** An example illustrating incorporating multiple modeling techniques. _Italicized text_ denotes the section that have been re-modeled using new techniques. 

**Postprocessing and Filtering** At the end of each iteration, OR-Instruct implements correction and filtering measures on the generated examples. First, we apply a regular match correction function to address minor grammatical errors in the programs, which may arise from GPT-4’s limited familiarity with the COPT API. Unexecutable programs are discarded, as they clearly represent low-quality data. Notably, in the final iteration, we also eliminate duplicate questions and any examples overlapping with the evaluation benchmarks to ensure the dataset remains uncontaminated. 

Based on manual sampling assessments, we find that the accuracy of the synthesized data by expansion operation is about 70% and 75% for the augmentation data, judged by the correctness of both the code and the model. On average, each iteration filters out approximately 39% of the generated examples, with the remaining examples incorporated into our training data pool. 

In summary, the above outlines all the key steps of OR-Instruct, and the specific procedures can be found in Figure 2. 

### **4. Results** 

In this section, we train the open-source 7b size large language models with synthetic data from ORInstruct and compare the results with GPT-4 as well as other benchmarks. Then, using the case of mixed integer linear programming as an example, we demonstrate the customized enhancement effect of OR-Instruct by including directionally generated training data. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

16 

#### **4.1. Data Generation by Using** OR-Instruct 

In our experiment, we initiate the study with 686 cases derived from previous industry projects, which the team engages with previously. These cases are abstracted and anonymized appropriately. Throughout the OR-Instruct process, we utilize the proprietary LLM `gpt-4-0613` as the standard model. For each cycle, the training data pool undergoes an expansion procedure 20,000 times and each augmentation operation is applied 6,000 times. Subsequently, an automatic filtration system excludes low-quality entries. After completing two iterations of this framework, we amass a total of 32,481 training examples. 



<!-- Start of picture text -->
Customer<br>Financial Services Transportation Service EntertainmentLegalConstructionSoftwareOthers Mixed Integer Programming37% ProgrammingQuadratic 2% Dynamic&Stochastic Programming2%<br>Education<br>Linear  Multi-objective  Others<br>Manufacturing Programming Programming3% 2%<br>Environment 19% ProgrammingInteger  ProgrammingNonlinear<br>30% 5%<br>Retail Public Utilities<br>Health Energy Agriculture<br>(a) Distribution of industies (b) Question type<br>Figure 7 Statistics of the data generated by OR-Instruct<br><!-- End of picture text -->

**Statistics:** Figure 7 presents the statistics of the OR-Instruct Data. Of the data, 57% is generated by the expansion operation, 17.2% by the augmentation of altering objectives and constraints, 15.3% by the augmentation of rephrasing questions, and 10.5% by the augmentation of incorporating multiple modeling techniques. For scenario diversity, we have abstracted 16 industries from a total of 1,556 expanded scenarios to facilitate their representation in a plot. Regarding question type diversity, it expands to 8 question types. In terms of data quality, the accuracy of correctness are 70% for expansion data and 75% for augmentation data. We find these accuracy acceptable in exchange for automatic filtering and more cost-effective data synthesis. Additionally, our preliminary experiments have demonstrated the benefits of incorporating such data. 

#### **4.2. Model Finetuning and Inference** 

This paper employs instruction tuning for open-source large models, a technique designed to enhance the ability of large language models (LLMs) to follow diverse natural language instructions. The primary aim is to improve zero-shot performance on unseen tasks, facilitating effective generalization across various instruction-based scenarios. The methodology involves training on a dataset of instruction-output pairs, typically consisting of three elements: an instruction (e.g., "Translate this 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

17 

sentence from English to Spanish"), optional context, and the target output. The training can be mathematically represented as: 



where _L_ ( _θ_ ) is the loss function, _x_ is the instruction input, _y_ is the expected output, and _θ_ denotes the model parameters. We borrow a widely used training framework from open-instruct (Wang et al. 2023d), where we take a natural language OR problem wrapped in an Alpaca-like template (Taori et al. 2023.) as the input prompt (see Appendix A.4), and treat a complete solution including mathematical models and programs as the target completion. 

During training, we compute the loss only over the target completion. We employ the ORInstruct dataset to train several open-source large language models (LLMs) of approximately 7 billion parameters, including Mistral-7B (Jiang et al. 2023), Deepseek-Math-7B-Base (Shao et al. 2024), and LLaMA-3-8B (AI@Meta 2024), which serve as our backbone models. We conduct a grid hyper-parameter search for each backbone and present the best-performing hyperparameters in Table 1.<sup>1</sup> The models resulting from this process are referred to as ORLMs. 

Regarding the inference techniques during evaluation, it is important to consider that large language models, as probabilistic generative models, exhibit inherent randomness. This randomness can lead to inconsistent outcomes across multiple evaluations. To mitigate the influence of this randomness, we implemented a greedy decoding strategy in a zero-shot scenario, consistently selecting the highest probability output (top-1) as the final result. After obtaining these results, we executed the corresponding code to derive the predicted optimal values for comparison with the ground truth. Although this greedy approach may reduce the performance of large models on such tasks, it ensures the stability of the output and enables the reproducibility of our findings under identical conditions. We will discuss the impact of employing additional inference techniques on the performance of large models in Section 5.4. 

**Table 1** Hyper-parameters for training ORLMs. 

|**Backbone**|**BatchSize**|**LearningRate**|**Epochs**|
|---|---|---|---|
|Mistral-7B|512|3e-6|2|
|Deepseek-Math-7B-Base|128|2e-5|2|
|LLaMA-3-8B|64|5e-6|2|
|Qwen-2.5-7B|64|2e-5|2|



> 1 Prior to the final fine-tuning, we conducted a grid search with learning rates within {2e-5, 5e-5, 7e-5, 3e-6, 5e-6, 7e-6}, batch sizes within {64, 128, 256, 512}, and training epochs within {1, 2, 3} to determine the optimal settings. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

18 

#### **4.3. Evaluation and Baselines** 

**Evaluation Benchmarks and Metrics:** We use NL4OPT (Ramamonjison et al. 2023.), MAMO (Huang et al. 2024b.), and IndustryOR as evaluation benchmarks. NL4OPT is the most widely used benchmark for operations research and includes 289 linear programming problems in its test set. However, NL4OPT only provides mathematical models as targets, which complicates the verification of execution accuracy due to the absence of optimal solutions. To address this, we convert these mathematical models into programs using GPT-4, calculate and check the optimal solutions, and use these as ground truth. MAMO, a concurrent project, evaluates the mathematical modeling capabilities in LLMs. It includes 652 easy and 211 complex linear programming problems, each paired with its corresponding optimal solution, sourced from various academic materials. IndustryOR, which is proposed in this work, is the first industrial benchmark, consisting of 100 real-world OR problems from eight industries. It covers 5 types of questions, linear programming, integer programming, mixed integer programming, non-linear programming, and others across 3 levels of difficulty. We measure performance using execution accuracy, where an executed optimal value that matches any provided ground truth optimal value is considered correct. Compared to NL4OPT, this metric enables a fully automated evaluation and provides greater flexibility for mathematical modeling approaches. 

**Baselines:** To ensure a comprehensive evaluation, we select a diverse set of models from previous methods for comparison. We include tag-BART (Kani and Gangwar 2022), which secured the first place in the NeurIPS competition (Ramamonjison et al. 2022). Additionally, we consider methods that utilize proprietary LLMs. The "standard" prompting method involves prompting a proprietary LLM to produce mathematical programs, serving as a fundamental baseline. We also incorporate complex prompt engineering methods such as Reflexion (Shinn et al. 2023), Chain-of-Experts (Xiao et al. 2023), and OptiMUS (AhmadiTeshnizi et al. 2024). These methods employ agents to refine both mathematical models and programs, achieving good performances on NL4OPT. We report their performance based on GPT-3.5 and GPT-4, respectively. Note that we implement the standard prompting on IndustryOR using the toolkit released by Chain-of-Experts (Xiao et al. 2023). 

In addition, we introduce the most well-known open-source large models for comparison, including Llama-3.1-lnstruct (Dubey et al. 2024), DeepSeek-v2-Chat (DeepSeek AI 2024), DeepSeek-R1 (Guo et al. 2025), Qwen2-Instruct (Qwen Team 2024), and Mistral-Nemo (Mistral AI 2024). Each model is tasked with constructing optimization models and generating code to solve the test set problems. 

We also assess the difference between the performance of ORLM and human-level performance. Given that constructing and solving optimization models requires a solid foundation in operations research and programming skills, we recruit 8 highly capable senior undergraduate students from relevant fields and 8 experts in the domain to evaluate four types of test sets. Each test set is 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

19 

evaluated by 2 senior undergraduate students and 2 experts. Each participant randomly selects 70 questions from their corresponding test set and is required to construct an optimized model and calculate the optimal solution. Participants are allowed to use any programming language; however, to ensure fairness in comparison with large models, they are only permitted to submit a finalized version of their code for testing and cannot make further modifications. Finally, the accuracy rates for the student and expert groups on each test set are obtained by averaging the results. 

**Table 2** Comparison of performance on the NL4OPT, MAMO, and IndustryOR benchmarks. Values marked with a<sup>*</sup> are directly copied from original papers, with blanks where data were not reported. The highest results are highlighted in bold. 

|**Method/Model**|**Size**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR**</sup>|**Micro**<br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|||_Method_<br><sup>*</sup>|_s based on _|_PLMs_||||
|tag-BART|140/400M|47.9%|-|-|-|-|-|
|||_Methods _<br><sup>*</sup>|_based on G_|_PT-3.5_||||
|Standard|Unknown|42.4%|-|-|-|-|-|
|Reflexion|Unknown|50.7%<sup>*</sup>|-|-|-|-|-|
|Chain-of-Experts|Unknown|58.9%<sup>*</sup>|-|-|-|-|-|
|||_Methods_<br>|_based on _<br>|_GPT-4_<br>||||
|Standard|Unknown|47.3%<sup>*</sup>|66.5%<sup>*</sup>|14.6%<sup>*</sup>|28.0%|50.2%|39.1%|
|Reflexion|Unknown|53.0%<sup>*</sup><br>|-|-|-|-|-|
|Chain-of-Experts|Unknown|64.2%<sup>*</sup><br>|-|-|-|-|-|
|OptiMUS|Unknown|78.8%<sup>*</sup>|-|-|-|-|-|
||_Stand_|_ard prompting_|_based on _|_open-source LL_|_Ms_|||
|Llama-3.1-Instruct|405B|38.7%|35.1%|20.8%|13.0%|31.5%|26.9%|
|DeepSeek-V2-Chat|236B|66.5%<br>|60.5%<br>|32.7%<br>|16.0%<br>|53.1%<br>|43.9%<br>|
|Qwen2-Instruct|72B|72.6%|79.9%|29.0%|18.0%|64.4%|49.8%|
|DeepSeek-R1-Distill|32B|80.4%|69.1%|**45.4%**|33.0%|64.8%|56.9%|
|Mistral-Nemo|12B|14.6%|19.4%|3.7%|7.0%|14.6%|11.1%|
|||_ORLMs based_|_on open-_|_source LLMs_||||
|ORLM-Mistral|7B|84.4%|81.4%|32.0%|27.0%|68.8%|56.2%|
|ORLM-Deepseek-Math|7B|**86.5%**|82.2%|37.9%|33.0%|71.2%|59.9%|
|ORLM-LLaMA-3|8B|85.7%|82.3%|37.4%|**38.0%**|71.4%|**60.8%**|
|ORLM-Qwen2.5|7B|86.1%|**85.2%**|44.1%|25%|**73.7%**|60.1%|
|||_Hum_<br>|_an Evalua_<br>|_tion_<br>||||
|Senior Undergraduates|-|80.4%|84.9%|53.1%|44.0%|75.2%|65.6%|
|Experts|-|94.3%|90.4%|78.9%|76.0%|85.0%|88.2%|



The results are presented in Table 2. First, it is clear that methods based on LLMs generally outperform the PLM-based best method (tag-BART) in the NL4OPT test. This suggests that PLMs have limited generalization capabilities. For proprietary LLMs, as the mathematical reasoning capability increases from GPT-3.5 to GPT-4, we observe that performance has advanced across all prompt engineering methods. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

20 

Our best-performing ORLMs, like ORLM-LLaMA-3 and ORLM-Qwen2.5, achieve state-of-the-art performance across four benchmarks with respect to GPT-4 and other open-source LLMs<sup>2</sup> , surpassing Standard prompting based on GPT-4 by 42.2% in micro average<sup>3</sup> and 55.4% in macro average<sup>4</sup> A comparison with human evaluation results reveals that ORLMs outperform senior undergraduate students on simpler problems (NL4OPT/MAMO-EasyLP) and approach expert-level performance. However, for more complex problems (IndustryOR/MAMO-ComplexLP), ORLMs still underperform relative to the average student, indicating that their problem-solving capabilities for complex tasks remain inadequate. We will analyze the underlying reasons for this in Section 5, highlighting that ORLMs still have the potential to surpass student performance and approach expert-level solutions on more challenging problems. 

While ORLMs demonstrate strong performance in optimization modeling tasks, we also evaluate their efficacy on general large language model benchmarks after domain-specific fine-tuning. In particular, we conduct a rigorous evaluation of the LLaMA-3-8B model (pre-fine-tuning) and the ORLM-LLaMA-3-8B model (post-fine-tuning) following the open-instruct (Wang et al. 2023d) on benchmarks from various domains, including mathematics (GSM8K), code (HumanEval), and general knowledge (MMLU, BBH, TydiQA), the results are listed in Table 3. 

**Table 3** Comparison of accuracy rate between LLaMA-3-8B and ORLM-LLaMA-3-8B across multiple benchmark 

domains. 

|**Model**|**GSM8K **|**HumanEval **|**MMLU **|**BBH **|**TydiQA**|
|---|---|---|---|---|---|
|LLaMA-3-8B|56.5%|67.7%|65.2%|63.7%|21.1%|
|ORLM-LLaMA-3-8B|58.0%|70.6%|64.6%|61.9%|21.9%|



The results reveal that ORLM-LLaMA-3-8B exhibits improved performance in the mathematics and coding domains, which aligns with expectations, as the OR-Instruct data emphasizes mathematical modeling and coding with solver assistance. However, the model exhibits a slight decline in general domain performance. Overall, the average performance across all domains shows no substantial deviation. 

**A comparative study on problem-solving efficiency.** To verify the effectiveness of ORLM in human–AI collaboration, we conduct a comparative experiment to demonstrate its impact on 

> 2 Due to the severe scarcity of API resources, we are unable to conduct large-scale modeling tests on many state-ofthe-art LLMs, such as DeepSeek-R1 (671B). 

> 3 Micro average aggregates the outcomes of all classes to compute the metrics, heavily weighing the classes with more instances. This method is effective for evaluating the overall effectiveness of the model, particularly in datasets where some classes significantly outnumber others. 

> 4 Macro average calculates individual metrics for each class without regard to class frequency, and then averages these metrics, treating all classes with equal importance. This approach highlights model performance on minority classes and is beneficial for assessing model fairness across diverse class distributions. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

21 

algorithm engineers in solving practical problems. Specifically, we recruit a group of 30 people, consisting of experts and senior undergraduate students, dividing them evenly into two groups, A and B. Each group comprises 7 experts and 8 undergraduate students, with comparable proficiency levels. We design 7 problems with varying difficulty levels, ranging from textbook exercises to those approximating industrial complexity. Group A is tasked with independently modeling and programming the solutions without the aid of ORLM, while Group B utilizes ORLM for problemsolving and programming. We assess the effectiveness of ORLM based on two dimensions: accuracy and solution time. The results are presented in Figure 8. We acknowledge that the sample size of the experiment is limited due to the difficulty of finding suitable subjects; nevertheless, we perform statistical analysis on the limited data and find that the comparison is still statistically significant. In the following, we detail our statistical analysis. 



<!-- Start of picture text -->
Group A 1.0 Group A<br>225 Group B Group B<br>Mean & 95% CI Mean & 95% CI<br>0.9<br>200<br>0.8<br>175<br>150 0.7<br>125 0.6<br>100 0.5<br>75 0.4<br>50<br>0.3<br>Total Expert Student Total Expert Student<br>Categories Categories<br>(a) Comparison of solution time (b) Comparison of accuracy<br>Accuracy (%)<br>Solution Time (min)<br><!-- End of picture text -->

**Figure 8** A comparative study on problem-solving efficiency 

Table 4 shows the results of our statistical analysis. Specifically, for each metric (difference in accuracy for total/experts/students, difference in time for total/experts/students), we first select an appropriate statistical test based on the distributional properties of the data, as indicated in the third column of the table. For solution time of each subgroup, we find that the distribution successfully passes the normality test and meets the assumption of homogeneity of variance. Consequently, we employ a standard t-test for statistical analysis. In contrast, for accuracy, the distribution does not conform to normality; therefore, we utilize the Mann-Whitney U test as a non-parametric alternative (see Hogg et al. 2019 for reference). Subsequently, we compute the test statistic and the corresponding _p_ -value for each test, which are reported in the 4th and 5th columns, respectively. We also calculate the 95% confidence interval for the difference between the two groups based on each test and present the results in the 6th column. 

To further demonstrate the robustness of our results, the last two columns provide additional analyses, including the effect size (Hedge’s g) and the statistical power (Cohen 2013). Notably, 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

22 

Hedge’s g is independent of sample size, making it a more objective measure of the generalizability and strength of the statistical significance. Meanwhile, statistical power serves as an indicator of the reliability and accuracy of our results. The detailed testing procedures and statistical indicators are provided in Appendix A.6. 

**Table 4** Summary of tests and effect sizes 

|Type|Test|Method|||Statistic Testin|g||
|---|---|---|---|---|---|---|---|
||||Stat|_p_-value|Confidence Interval|Hedge’s g|Stat Power|
|Total|Accuracy|Mann-Whitney U test|192.00|0.001|(0.14, 0.24)|1.46|0.97|
||Time|Mann-Whitney U test|0.00|0.000|(-134.02, -112.35)|-4.43|1.00|
|Expert|Accuracy|Mann-Whitney U test|44.00|0.008|(0.10, 0.25)|1.81|0.87|
||Time|t-test|-22.50|0.000|(-117.61, -96.85)|-11.26|1.00|
|Student|<sup>Accuracy </sup>|<sup>Mann-Whitney U test</sup>|56.5|0.006|(0.14, 0.26)|1.56|0.82|
||Time|t-test|-20.27|0.000|(-151.29, -122.34)|-9.58|1.00|



> a) For the criteria used in selecting between the _Mann-Whitney U test_ and the _independent samples t-test_ , please refer to Appendix A.6. 

For Table 4, we can see that at a 95% confidence level, the use of ORLM significantly improves both solution time and accuracy across all populations (total, expert, and student samples). The confidence intervals suggest that, after implementing ORLM, accuracy improves by approximately 10%–25%. Additionally, the total time saved in solving optimization modeling problems is 1.8–2.2 hours, with experts saving approximately 1.5–2 hours and students saving around 2–2.5 hours. The absolute value of Hedge’s g _>_ 1 indicates a substantial effect size, highlighting a large difference between experimental and control groups. Additionally, statistical power _>_ 0 _._ 8, ensuring a high probability of detecting a true effect and minimizing Type II error risk. 

In addition, we collect feedback from engineers on their experience using ORLM, as shown in Table 5. None of the engineers rate ORLM as "useless" or "minimal help". Instead, the majority provide highly positive evaluations ("significant help" or "highly effective"), indicating that ORLM is both efficient and effective in assisting their work. These demonstrate the significant potential of ORLM to enhance the application of operations research in industry through human–AI collaboration. We will further discuss the application value of ORLM in Section 6.1. 

**Table 5** Feedback from participants on ORLM effectiveness 

|Category|Useless|Minimal Help|Moderate|Help|Significant|Help Highly Effective|
|---|---|---|---|---|---|---|
|Percentage (%)|0.0|0.0|13.3||60.0|26.7|



**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

23 

#### **4.4. Customization Enhancement** 

In this subsection, we illustrate the capability of our framework to enhance large models in specific areas by generating targeted types of optimization modeling data. Specifically, we focus on the scenario of mixed integer linear programming (MILP). We provide an empirical example demonstrating how the quality of responses improves with training. Initially, we use a base dataset comprising 10,000 general modeling cases. To enhance the ORLM’s proficiency in MILP, we selected 50 fundamental MILP questions and their answers for inclusion in the seed data pool. After several iterative rounds, this process yields 2,000 tailored training data points for MILP. We will subsequently assess the impact of incorporating these 2,000 data points into the training dataset by comparing the ORLM’s performance before and after their addition. 



<!-- Start of picture text -->
GPT 4 General ORLM Enhanced ORLM<br>Mathematical Model: Mathematical Model: Mathematical Model:<br>To solve this problem, we can formulate it as a linear  To solve the optimization problem for the toy  To help the toy manufacturer maximize profit, we need<br>programming problem. We will define the decision  manufacturer, we constructed a linear programming  to construct an integer programming model to<br>variables, objective function, and constraints, then use a  model and used the `coptpy` library to solve it. This  determine the optimal production mix. Below is the<br>solver to find the optimal solution. model helps us maximize profit while meeting  model construction:<br>production conditions and resource constraints. Below  Decision Variables:<br>Decision Variables: are the detailed mathematical model and the solution  ▪ 𝑥𝑇: Number of toy trucks to be produced.<br>▪ 𝑥1: Number of toy trucks produced. script: ▪ 𝑥𝑃: Number of toy planes to be produced.<br>▪ 𝑥2: Number of toy airplanes produced. ▪ 𝑥𝑆: Number of toy ships to be produced.<br>▪ 𝑥3: Number of toy boats produced. Decision Variables: ▪ 𝑥𝑅: Number of toy trains to be produced.<br>▪ 𝑥4: be the number of toy trains produced. ▪ x1: Number of toy trucks produced. ▪ 𝑦𝑇 : Whether to produce toy trucks  (1 =<br>▪ x2: Number of toy airplanes produced.  𝑌𝑒𝑠, 0 = 𝑁𝑜).<br>Objective Function: ▪ x3: Number of toy boats produced. ▪ 𝑦𝑃 : Whether to produce toy planes  (1 =<br>▪ Maximize profit: Profit = 5𝑥1 + 10𝑥2 + 8𝑥3 + ▪ x4: Number of toy trains produced.  𝑌𝑒𝑠, 0 = 𝑁𝑜).<br> 7𝑥4 ▪ 𝑦𝑆: Whether to produce toy ships (1 = 𝑌𝑒𝑠, 0 =<br>Objective Function:  𝑁𝑜).<br>Constraints: ▪ Maximize  profit:  Z = 5x1 + 10x2 + 8x3 + ▪ 𝑦𝑅: Whether to produce toy trains (1 = 𝑌𝑒𝑠, 0 =<br>1. Wood constraint:  12𝑥1 + 20𝑥2 + 15𝑥3 + 10𝑥4 ≤  7x4  𝑁𝑜).<br>890  ▪ This function calculates the total profit based  Objective Function:  Maximize total profit:  𝑍 =<br>on the profit and quantity of each toy.  5𝑥𝑇 + 10𝑥𝑃 + 8𝑥𝑆 + 7𝑥𝑅<br>2. Steel constraint: 6𝑥1 + 3𝑥2 + 5𝑥3 + 4𝑥4 ≤500  Constraints:<br>Constraints: 1. Wood  usage  limit:  12𝑥𝑇 + 20𝑥𝑃 + 15𝑥𝑆 +<br>3. If trucks are manufactured, trains will not be  1. Wood  usage  limit:  12x1 + 20x2 + 15x3 + 10𝑥𝑅 ≤890<br>manufactured: 𝑥1 ⋅𝑥4 = 0   10x4 ≤ 890 2. Steel usage limit: 6𝑥𝑇 + 3𝑥𝑃 + 5𝑥𝑆 + 4𝑥𝑅 ≤500<br>2. Steel usage limit:  6x1 + 3x2 + 5x3 + 4x4 ≤ 3. Production condition 1:  𝑦𝑇 + 𝑦𝑅 ≤1 (If trucks<br>4. If boats are manufactured, airplanes will also be   500 are produced, trains will not be produced)<br>manufactured: 𝑥3 ≤𝑥2 3. Production conditions: 4. Production condition 2:  𝑦𝑃 ≥𝑦𝑆  (If ships are<br>4. If trucks are produced, trains will not be produced:  produced, planes will also be produced)<br>5. The number of toy boats manufactured cannot exceed  x1 + x4 ≤1 5. Production condition 3:  𝑥𝑆 ≤𝑥𝑅 (The number of<br>the number of toy trains manufactured: 𝑥3 ≤𝑥4 5. If boats are produced, airplanes will also be  toy ships produced cannot exceed the number of<br>produced: x3 ≤ x2 toy trains produced)<br>6. Non-negativity constraints: 𝑥1, 𝑥2, 𝑥3, 𝑥4 ≥0  6. The number of toy boats produced cannot exceed  6. Logical relationship for production:<br>the number of toy trains produced: x3 ≤ x4 a) 𝑥𝑇 ≤𝑀⋅𝑦𝑇<br>b) 𝑥𝑃 ≤𝑀⋅𝑦𝑃<br>Non-negativity Constraints: c) 𝑥𝑆 ≤𝑀⋅𝑦𝑆<br>x1, x2, x3, x4 ≥0, and they should be integers to ensure  d) 𝑥𝑅 ≤𝑀⋅𝑦𝑅<br>practical integer solutions. Where 𝑀 is a sufficiently large number to ensure that if<br>a toy type is not selected for production, the<br>corresponding production quantity is zero.<br><!-- End of picture text -->

**Figure 9** Comparison of ORLM before and after adding specific data for training and GPT-4 responses, the code part is omitted here. Incorrect responses are marked in red. 

As depicted in Figure 9, in response to the scenario presented in Figure 1, GPT-4 inaccurately interprets logical relationships as quantitative ones and includes nonlinear terms during the modeling process as shown in the red area, adversely affecting solver performance. A similar mistake is observed in the general ORLM, which also misinterprets logical relationships as quantitative. In contrast, the 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

24 

targeted-trained ORLM accurately transforms the problem into a correct mathematical model by utilizing indicator variables and the Big _M_ method. This showcases the robust generalization capability of OR-Instruct. Furthermore, OR-Instruct not only facilitates customized improvements across different modeling types but also demonstrates potential for targeted enhancements within specific industrial sectors. 

### **5. Analysis and Discussion** 

#### **5.1. Detailed Comparison of ORLM vs GPT-4 on IndustryOR** 

To assess the optimization modeling capabilities across different levels of difficulty and question types, we compare the accuracy rate of ORLM-LLaMA-3-8B and Standard-GPT-4 on IndustryOR, as shown in Figure 10. ORLM-LLaMA-3-8B shows superior performance over Standard-GPT-4 across all difficulty levels, especially in the hard category. Regarding different question types, ORLM-LLaMA3-8B outperforms Standard-GPT-4 in linear programming, integer programming, and mixed-integer programming. Both models perform poorly in non-linear programming and other rare question types. This is partly due to the fact that the seed dataset collected contains too few examples of nonlinear and other types of optimization modeling, resulting in a low percentage of that type in the training dataset, and partly due to the fact that the inherent complexity and scarcity of these types of questions. Overall, the OR-Instruct data proves effective in enhancing _Comprehensive Coverage_ across various question types and difficulty levels. 



<!-- Start of picture text -->
60 57.5% 61.2%<br>Methods 60 Methods<br>Standard-GPT-4 Standard-GPT-4<br>50 ORLM-LLAMA-3 8B ORLM-LLAMA-3 8B<br>45.0% 50<br>40<br>35.0% 40 36.1% 38.7%<br>33.3%<br>30<br>30<br>20.0%<br>20 17.5% 20 19.3%<br>15.0%<br>12.9%<br>10 10<br>0.0% 0.0% 0.0% 0.0%<br>0 0<br>Easy Medium Hard LP NLP IP MIP Others<br>Difficulty Question Types<br>Percentage Percentage<br><!-- End of picture text -->

**Figure 10** Accuracy rate of ORLM and GPT-4 on IndustryOR across different difficulty levels and question types. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

25 

#### **5.2. Ablation Study** 

**Ablation Study on Data Synthesis Strategy** We first assess whether the data generated by OR-Instruct truly leads to improvements in the Seed data, particularly in terms of the performance of the ORLM. Particularly, we compare the performance of fine-tuning on seed data alone with the results of fine-tuning on OR-Instruct-generated data based on the same seed data. We observe that, with the exception of minor variations in simpler linear programming cases (MAMO_EasyLP), the OR-Instruct-generated data yield a significant performance boost for ORLM than only using the seed data as shown in Table 6. 

**Table 6** Performance comparison with varying data sizes 

|**Base Model**|**Data Size**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR**</sup>|**Micro**<br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|LLaMA-3-8B|32,481 (Full data)|85.7%|82.3%|37.4%|38.0%|71.4%|60.8%|
|LLaMA-3-8B|686 (seed data)|75.1%|82.8%|29.4%|20.0%|67.0%|51.8%|



**Ablation Study on** OR-Instruct **Augmentations** To further verify the effectiveness of the augmentations in OR-Instruct, we conduct detailed ablation experiments to study the effects of altering objectives and constraints, rephrasing questions, and incorporating multiple modeling techniques. Specifically, we construct four distinct datasets, each comprising 3,000 instances, drawn from the OR-Instruct data but employing different augmentation strategies. These datasets are then utilized to train the LLaMA-3-8B model, maintaining consistent hyperparameters across all experimental conditions. The results are presented in Table 7. Training data with all three augmentations (denoted as Full Augmentations) achieves a base performance of 68.6% in micro average and 55.7% in macro average. Removing any of the three augmentations from the base setting leads to a performance drop across all benchmarks, both in micro and macro averages. Rephrasing questions seems slightly more important than the other two. Overall, the results show that all three augmentations contribute to general performance, proving their effectiveness in enhancing the _data diversity_ . 

**Table 7** Ablation study on OR-Instruct augmentations. 

|**Method**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR **</sup>|<sup>**Micro**</sup><br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|
|Full Augmentations|78.3%|80.6%|43.1%|21.0%|68.6%|55.7%|
|w/o Altering Obj&Const|77.5%|79.2%|36.4%|20.0%|66.4%|53.2%|
|w/o Rephrasing Questions|74.2%|77.3%|41.1%|15.0%|65.1%|51.9%|
|w/o Multiple Modeling|78.3%|78.0%|38.8%|18.0%|66.2%|53.2%|



**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

26 

**Ablation Study on Question Types** ORLM can be tailored to specific domains within the field of optimization, depending on its initial training dataset. _A key consideration in this process is whether incorporating data from other domains is necessary._ This investigation aims to provide valuable guidance for implementing ORLM in specialized areas. 

We use linear programming as a case study, comparing ORLM’s performance when trained solely on linear programming data versus a mixed dataset including other problem types. Specifically, we construct two training sets, each comprising 7,049 instances: one set exclusively consisting of pure linear programming (LP) problems, and the other comprising a diverse mixture of problem types<sup>5</sup> We fine-tune the Meta-Llama3 8B model on both datasets, ensuring that hyper-parameter settings remain consistent across experiments. The test performance is summarized in Table 8: 

**Table 8** Performance of ORLM-LLaMA-3-8B on different datasets 

|**Dataset **|**Data Size**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR **</sup>|<sup>**Micro**</sup><br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|LP Only|7,049|82.0%|77.4%|26.1%|20.0%|65.4%|51.4%|
|Mixed|7,049|86.5%|81.2%|34.6%|21.0%|69.8%|55.8%|



As illustrated in Table 8, even with identical test sizes, the inclusion of mixed problem types significantly enhances the performance of the ORLM-LLaMA-3-8B across various datasets. Notably, when examining the tests focused on linear programming, specifically MAMO-EasyLP and MAMOComplexLP, it is evident that integrating additional problem types is more effective in enhancing the ORLM’s performance on challenging linear programming problems. A plausible explanation for this phenomenon is that the incorporation of a broader variety of problems effectively strengthens the generalization ability of the ORLM-LLaMA-3-8B, allowing it to capture a wider modeling capacity and consequently improve modeling performance (See Dong et al. 2023). 

#### **5.3. Scaling Laws** 

The concept of scaling laws is a key element in the development of large models. It refers to the phenomenon that the performance of large language models improves as their size and complexity increase. In this section, we will examine the impact of scaling laws on ORLMs from two dimensions: training data and model size. 

From the perspective of training data, we begin with seed data and subsequently randomly sample a predetermined number of training data from the data generated by OR-Instruct. Using the LLaMA-3-8B model as the base, we conduct training while keeping all other hyperparameters 

> 5 This dataset is comprised of 35% linear programming, 40% mixed integer programming, 25% other types. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

27 

constant (as in Table 1), in order to observe the performance of ORLM-LLaMA-3-8B on various test sets. Regarding model size, we focus on the Qwen large model series, as it offers a more refined range of model sizes that are compatible with our hardware limitations (0.5B, 1.5B, 3B, 7B, 14B). We fix the training dataset to be all data generated by OR-Instruct. Under the condition of identical training hyperparameters, we observe the performance of different Qwen2.5 model sizes on various test sets. In our study, we use the overall macro average and micro average across four test sets as metrics to evaluate the performance of the ORLMs, as visualized in Figure 11. More detailed results are provided in Appendix A.5.2. 



<!-- Start of picture text -->
75<br>70<br>70<br>65 65<br>60<br>60<br>55<br>55 50<br>Micro Avg<br>50 Macro Avg 45 Micro Avg<br>Macro Avg<br>40<br>0.5 1.5 3.0 7.0 14.0<br>Data Size Model Size (Billion)<br>(a) Different sizes of training sets (b) Different sizes of base models<br>0 3000 6000 9000 12000 15000 18000 21000 24000 27000 30000<br>AverageScore<br>AverageScore<br><!-- End of picture text -->

**Figure 11** Scaling law validation across different data and model sizes 

The figure clearly shows an upward trend in ORLM’s accuracy on the test sets as either the model size or the data volume increases. However, the impact of these two types of scaling laws on ORLM’s performance differs. Specifically, increasing the training set size results in fluctuating performance gains from the macro average metric, this is because for simple test datasets (NL4OPT and MAMOeasyLP), ORLM quickly reaches a performance bottleneck and begins to fluctuate, causing instability in its accuracy across the entire dataset. For micro average metric, the overall performance continues to exhibit a monotonic increase with the expansion of training data, approximately following a power-law trend. This indicates that increasing the amount of training data remains beneficial for improving the model’s capabilities. 

Regarding the scaling law for model size, it is evident that increasing the model size significantly enhances ORLM’s accuracy. This increase not only yields steady incremental gains but also follows a power-law trend, consistent with the findings reported by Kaplan et al. (2020). This indicates that the intrinsic capability of the base model establishes a higher performance ceiling for ORLMs in optimization modeling tasks. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

28 

#### **5.4. Inference Techniques** 

In previous model evaluations, we employed a greedy inference strategy to ensure the replicability and fairness of the results. However, using greedy sampling entails always selecting the word with the highest probability from the large model’s output during each generation. While this approach guarantees deterministic results, it also limits the model’s diversity and creativity. To address this, in this section, we will utilize more common sampling techniques to assess the performance improvements of the ORLMs. Specifically, we adjust the following two parameters: First, the _temperature_ parameter controls the diversity of the generated text. Higher temperature values increase the randomness and creativity of the generated content, while lower values tend to produce more deterministic text. Second, the _top-P_ parameter restricts the range of vocabulary choices considered by the model during generation. A higher _top-P_ value means the model will consider a broader set of candidate words, thus enhancing the diversity of the generated content. To avoid excessive randomness that may lead to significant fluctuations in the accuracy of the generated results, we apply _Pass@k_ ( _k_ = 2 _,_ 4 _,_ 8) strategy to enhance stability. Specifically, for each query, the large model generates top _k_ candidate answers, and as long as at least one of the top _k_ answers is correct, it is considered to have answered this question correctly (Pass@ _k_ ). This approach helps improve the consistency and stability of the generated outcomes. The test results is detailed in Table 9. 

**Table 9** Performance of ORLM-LLaMA-3-8B on different decoding methods 

|**Model**|**Inference**<br>**Settings**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR**</sup>|**Micro**<br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|ORLM-LLaMA-3-8B<br>ORLM-LLaMA-3-8B|pass@1,<br>temp=0,<br>top-P=1.0<br>pass@2,<br>temp=0.7,<br>top-P=0.95<br>pass@4,|85.7%<br>88.6%|82.3%<br>83.7%|37.4%<br>49.8%|38.0%<br>40.0%|71.4%<br>75.6%|60.8%<br>65.5%|
|ORLM-LLaMA-3-8B|temp=0.7,<br>top-P=0.95<br>pass@8,|91.4%|85.9%|56.9%|44.0%|78.9%|69.6%|
|ORLM-LLaMA-3-8B|temp=0.7,<br>top-P=0.95|93.0%|88.4%|72.1%|49.0%|83.6%|75.6%|



Significant improvements have been observed in ORLMs across four test sets, with the overall micro average of Pass@8 increasing by 17.09% relative to the previous version, while the macro average rose by 24.34%. A comparison with Table 2 reveals that, in terms of both macro average and micro average accuracy, the ORLM under the Pass@8 strategy has already surpassed the accuracy of senior undergraduate students and is approaching that of experts. This highlights the significant potential of ORLMs to serve as a viable alternative to human engineers. The high Pass@8 score 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

29 

indicates that the correct answer is often found within the top 8 solutions. However, the model’s greedy decoding strategy remains insufficiently effective to consistently prioritize the optimal answer. The notable progress between the Pass@1 and Pass@8 scores suggests that while the model has the potential to generate correct solutions, its ranking capability is currently inadequate to reliably place the optimal solution in the first position. Fortunately, reinforcement learning may offer a promising solution to bridge the gap between Pass@1 and Pass@8, we will discuss it in the future work (See Section 6.2). 

#### **5.5. Limitations Analysis** 

Building upon the previous discussion and results, this section concludes with an analysis of the current limitations of ORLM. First, using ORLM-Llama-3-8B as a case study, we present a statistical breakdown of error types under the greedy inference strategy, as shown in Table 10. 

**Table 10** Error frequency across different datasets 

|**Error Type**|**NL4OPT **|<sup>**MAMO**</sup><br>**Easy**|**MAMO**<br>**Complex**|**IndustryOR**|**Overall**<br>**Percentage**|**Error**<br>**Percentage**|
|---|---|---|---|---|---|---|
|Code Error|1.04%|0.00%|16.59%|31.00%|5.51%|19.77%|
|Model Error|12.46%|17.64%|45.97%|31.00%|22.28%|80.23%|



In the table above, the "Overall Percentage" represents the occurrence frequency of each error type across all test sets, while the "Error Percentage" indicates the proportion of each error type within the total number of errors. The data reveals that, ORLM has demonstrated considerable proficiency in utilizing COPT, achieving a pass rate of approximately 95% across more than 1,000 test cases. Consequently, the primary challenges lie in the optimization modeling phase of the process. 

To analyze the types of errors occurring in ORLM modeling, we randomly selected 100 problems from those where ORLM failed. Following manual evaluation and statistical analysis, and after excluding errors caused by coding issues, we categorized the modeling-related errors into three primary types, as detailed in Table 11. Notably, the predominant cause of ORLM’s modeling errors is "Low Model Completeness", which accounts for more than half of the observed errors. Further analysis reveals that this issue stems from the limitations in the expressive and learning capabilities of 8B-scale models. These models often produce overly simplified outputs in complex scenarios, reducing the intricacy of optimization modeling problems even when such scenarios are included in the training set. This highlights the importance of fine-tuning larger-scale models, a conclusion supported by our scaling law experiments. 

Although ORLM still has certain limitations, as demonstrated by previous experimental results, we recognize substantial opportunities for improvement through the application of scaling laws, 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

30 

**Table 11** Analysis of main mistakes in optimization modeling 

|**Modeling Error Type**|**Description**|**Proportion**|
|---|---|---|
|Semantic Misunderstanding <br>Errors in Objective/<br>Constraint Translation|Misunderstand the problem that the<br>optimization model needs to solve.<br>Correctly understand the requirements,<br>but make errors when formulating the<br>optimization model.|13.40%<br>30.30%|
|Low Model Completeness|Ignore some constraints or implicit con-<br>ditions of the real problem, simplifying<br>the complex problem.|56.30%|



different inference techniques and others. ORLM is still promising in addressing complex optimization modeling problems, even certain real-world industrial problems within specific domains. In the next section, we will demonstrate how ORLM can be applied to practical scenarios such as industrial production, education, and other real-world applications. 

### **6. Future Direction** 

In previous sections, we conduct a detailed analysis of ORLM’s strengths and limitations within the field of optimization modeling. In this section, we build on above experimental results to discuss the practical applications of ORLM and potential directions for future improvement. 

#### **6.1. Potential Applications** 

Large language models are increasingly influential across various industries, and the rise of privatized and domain-specific LLMs presents new topics for management. This work represents the first attempt to fine-tune open-source LLMs specifically for optimization modeling. The ORLM not only surpasses the performance of cutting-edge proprietary models but also ensures privacy, security, and stability for commercial applications. Additionally, its 7B size allows for private deployment on personal computers with only 16GB of VRAM, making operations research more accessible to a wider audience. We hope that this work could shed lights on the deep integration of large language models with operations research and management science. Potential applications are listed as follows: 

1. **Revolutionizing the role of operations research in industry** : In recent years, operations research has rapidly permeated various industrial sectors, supporting companies in making more informed and effective decisions. However, optimization modeling tasks in industry often encounter two critical challenges: (1) optimization models are typically not robust enough to withstand changes in external conditions. When the environment shifts, models must be quickly adjusted to help companies make timely decisions under new circumstances; (2) optimization projects typically rely on business experts to specify goals and constraints, while algorithm engineers are responsible for developing and solving the models. For many specialized industrial 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

31 

problems, communication between these two roles can be costly. Algorithm engineers may struggle to grasp the intricacies of business logic, and business experts often lack technical modeling expertise. 

The introduction of ORLM could help address many of these challenges. Particularly, companies with extensive training data can customize ORLMs to their domain based on OR-Instruct. As demonstrated in Tables 2 and 3, ORLM significantly enhances optimization modeling capabilities while retaining the broad knowledge acquired during pre-training. This allows it to quickly grasp industry-specific terminology and facilitate effective communication between business experts and algorithm engineers. ORLM operates with remarkable efficiency, generating an initial solution within seconds that both engineers and business teams can refer to. Given ORLM’s strong performance on Pass@8 metrics, it can also produce multiple solutions, supporting selection and comparison, which accelerates project iterations. Two representative workflows are illustrated in Figure 12. 



<!-- Start of picture text -->
ORLM<br>Original Scenario  𝐴𝟎 Confirm Variant of Original<br>Business User Algorithm Engineer<br>Original Optimization Model  𝑀�� Scenario  𝐴�<br>Modifies the model via ORLM Updated Optimization<br>Due to unforeseen  •Prompt：Now my scenario has changed, and I  Model  𝑀�� via ORLM<br>circumstances, it is necessary  need to additionally consider...<br>to incorporate daily  • Please add the objective function... and<br>availability of transport  the constraint...<br>vehicles and cost constraints  • Do not change the original definition of<br>into the model. • variables and parameters in the model.Please update the model.<br>(a) In the course of enterprise development, the constraints and objectives of operational<br>contexts continually evolve, necessitating swift adjustments to existing algorithmic<br>models to meet business demands.<br>ORLM<br>Business User<br>New Scenario B Algorithm Engineer Optimization Model  𝑴𝑩 Receive Feedback<br>• Quick modeling by using ORLM<br><!-- End of picture text -->

- (a) In the course of enterprise development, the constraints and objectives of operational contexts continually evolve, necessitating swift adjustments to existing algorithmic models to meet business demands. 

- (b) For newly arising decision-making problems, enterprises can leverage ORLM for rapid modeling and experiment with small data samples. This approach enables 

   - enterprises to respond swiftly to market changes. 

**Figure 12** Utilize ORLM for adaptive modeling in enterprise decision-making. 

Moreover, ORLM can seamlessly modify existing optimization models by adding new business constraints, creating preliminary models, and generating initial solution code, which engineers 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

32 

can then validate. This capability not only reduces delivery costs but also improves accuracy on complex tasks. 

Beyond these capabilities, ORLM has the potential to leverage Retrieval-Augmented Generation (RAG) and similar technologies to incorporate internal company documents, evolving into a domain-specific optimization expert well-versed in the company’s field. This feature allows ORLM to support knowledge transfer and updates, transforming traditional project reports into valuable data assets for future model training. In addition to project delivery, ORLM can also be applied in training junior algorithm engineers in modeling techniques, further enhancing its value within the enterprise. 

2. **Operations research education** : The outstanding performance of ORLM in fundamental optimization modeling problems makes it sufficiently capable of addressing the modeling challenges encountered by beginners in operations research. Instructors can utilize ORLM for efficient instructional guidance, allowing students to quickly derive reference solutions and processes for unfamiliar operations research modeling problems, thereby enhancing teaching efficiency and quality. 

3. **Mathematical modeling competitions** : As one of the most influential competitions, mathematical modeling contests aim to cultivate students’ abilities to solve problems using mathematical knowledge. Since 2023, several mathematical modeling competitions have begun to acknowledge the significant role of generative AI in modeling, permitting its use as an aid (e.g., MCM 2024). The capabilities of ORLM position it as a powerful tool in such competitions. 

4. **Reducing the learning cost of solvers** : Solvers are a core component of optimization modeling problems, yet the diverse programming syntax of different solvers significantly increases the learning cost for users, hindering their widespread adoption. The emergence of ORLM marks a pivotal shift in this regard. Notably, Table 10 indicates that ORLM rarely encounters errors due to coding issues (95% accuracy rate), even with less common syntax such as that specific to COPT. This suggests that algorithm engineers can confidently develop reliable operations research models and rely on ORLM to translate them into corresponding solver code, alleviating the need to extensively learn solver syntax. 

#### **6.2. Future Research Directions** 

In Section 5, we conduct extensive experiments to analyze the current limitations of ORLM and to investigate the underlying causes. Based on our findings, we propose directions for future improvements, calling for community attention and collaboration to drive progress in this field: 

- **Incorporating sophisticated techniques:** In Section 5.4, we observe that while ORLM can generate correct answers, it struggles with ranking them effectively. Incorporating reinforcement 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

33 

learning techniques could help narrow the gap between pass@1 and pass@8 scores. As noted by Sutton and Barto (2018), one of the primary goals of reinforcement learning is to align the policy with the Bellman optimality policy, effectively optimizing ranking quality. In this context, relevant methods like reinforcement learning from human feedback (RLHF), direct preference optimization (DPO), and Kahneman-Tversky optimization (KTO) aim to minimize the disparity between the model’s current greedy decoding policy and the Bellman optimality policy, thereby enhancing the model’s ranking accuracy and moving pass@1 closer to pass@8. In addition, approaches such as multi-agent collaboration and internal chain of thought structures similar to o1 (OpenAI 2024) could further enhance the performance of current large models in optimization modeling tasks. 

- **Dataset construction** : While this paper presents a data synthesis strategy, it is insufficient for reinforcement learning techniques like RLHF, which require training data in the form of a preference list. For each question, multiple responses must be ranked according to preference. Furthermore, in the context of optimization problems, incorporating actual optimal solutions into the training set would enable a wider range of techniques. Constructing such datasets may require user’s feedback or the development of new data synthesis methods to better meet these needs. 

- **Data mining and exploration** : As shown in Figure 11, we have demonstrated that scaling laws significantly benefit ORLM. However, for a fixed model size, the performance gains from additional data become increasingly marginal at later stages. This raises the question of whether it is possible to identify an optimized, minimal dataset or develop efficient data synthesis strategies that can balance ORLM’s performance with the associated training costs. Existing studies (e.g., Chen et al. 2023b) indicate that only a small portion of a complete dataset is often sufficient to achieve comparable performance. Therefore, developing a tailored data exploration strategy for optimization problem modeling, which minimizes the reliance on large-scale data resources for enhancing large models, represents an important direction for future research. 

### **7. Concluding Remarks** 

In this paper, we propose a new path for the training of open-source large language models (LLMs) specifically tailored for optimization modeling. We characterize four critical requirements essential for the training dataset of optimization modeling LLMs and develop OR-Instruct, a semi-automated framework for generating synthetic data that meets these specific needs. Additionally, we introduce the IndustryOR benchmark, the first of its kind in the industry. We utilize the OR-Instruct data to train open-source LLMs with approximately 7 billion parameters, which significantly enhances their optimization modeling capabilities, achieving competitive performance across all test datasets. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

34 

This paper also identifies the current limitations of ORLM, such as its overly simplistic output for complex problems, weak ability to rank optimal solutions, and poor learning capability from data. Our experiments suggest that ORLM can be further enhanced by leveraging scaling laws or incorporating methods such as reinforcement learning (RL), potentially reaching expert-level performance. We hope these findings provide valuable insights for the future advancement of ORLM’s applications in industry and open promising avenues for subsequent research. 

Finally, we note that during the revision process of this paper, numerous high-performing large models have emerged, such as DeepSeek-R1 and Grok-3. While these new models demonstrate impressive capabilities, further enhancing their performance in optimization modeling requires additional refinement. The framework proposed in this paper offers a valuable reference for such improvements, including synthesizing high-quality data to strengthen modeling comprehension, or considering reinforcement learning strategies to align ranking capabilities. By leveraging our framework as a promising starting point, the inherent strengths of large models can be more effectively translated into optimization modeling capabilities. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

35 

### **References** 

- Tamara Adams, Alessandro Ferrucci, Pedro Carvalho, Sothiara Em, Benjamin Whitley, Ryan Cecchi, Teresa Hicks, Alexander Wooten, John Cuffe, Stephanie Studds, et al. Advanced analytics drives reengineering of field operations for the 2020 US Census. _INFORMS Journal on Applied Analytics_ , 53(1):47–58, 2023. 

- Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. Optimus: Scalable optimization modeling with (MI)LP solvers and large language models. _arXiv preprint arXiv:2402.10172_ , 2024. 

- AI@Meta. Llama 3 model card. 2024. URL `https://github.com/meta-llama/llama3/blob/main/MODEL_ CARD.md` . 

- Laith Alzubaidi, Jinshuai Bai, Aiman Al-Sabaawi, Jose Santamaría, Ahmed Shihab Albahri, Bashar Sami Nayyef Al-dabbagh, Mohammed A Fadhel, Mohamed Manoufali, Jinglan Zhang, Ali H Al-Timemy, et al. A survey on deep learning tools dealing with data scarcity: Definitions, challenges, solutions, tips, and applications. _Journal of Big Data_ , 10(1):46, 2023. 

- Ali Aouad and Antoine Désir. Representing random utility choice models with neural networks. _arXiv preprint arXiv:2207.12877_ , 2022. 

- John Berry and Ken Houston. _Mathematical Modelling_ . Gulf Professional Publishing, 1995. 

- Hao Chen, Gonzalo E Constante-Flores, and Can Li. Diagnosing infeasible optimization problems using large language models. _arXiv preprint arXiv:2308.12923_ , 2023a. 

- Hao Chen, Yiming Zhang, Qi Zhang, Hantao Yang, Xiaomeng Hu, Xuetao Ma, Yifan Yanggong, and Junbo Zhao. Maybe only 0.5% data is needed: A preliminary exploration of low training data instruction tuning. _arXiv preprint arXiv:2305.09246_ , 2023b. 

- Tianlong Chen, Xiaohan Chen, Wuyang Chen, Howard Heaton, Jialin Liu, Zhangyang Wang, and Wotao Yin. Learning to optimize: A primer and a benchmark. _Journal of Machine Learning Research_ , 23(189):1–59, 2022a. 

- Yanguang Chen, Wenzhi Gao, Dongdong Ge, and Yinyu Ye. Pre-trained mixed integer optimization through multi-variable cardinality branching. _arXiv preprint arXiv:2305.12352_ , 2023c. 

- Yifei Chen, Bryan T Kelly, and Dacheng Xiu. Expected returns and large language models. _Available at SSRN 4416687_ , 2022b. 

- Yitian Chen, Yanfei Kang, Yixiong Chen, and Zizhuo Wang. Probabilistic forecasting with temporal convolutional neural network. _Neurocomputing_ , 399:491–501, 2020. 

- J. Cohen. _Statistical Power Analysis for the Behavioral Sciences_ . Routledge, 2nd edition, 2013. ISBN 9780367249737. 

- Jim G Dai and Mark Gluzman. Queueing network controls via deep reinforcement learning. _Stochastic Systems_ , 12(1):30–67, 2022. 

- DeepSeek AI. Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model. _GitHub Repository_ , 2024. URL `https://github.com/deepseek-ai/DeepSeek-V2` . 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

36 

- Bosheng Ding, Chengwei Qin, Ruochen Zhao, Tianze Luo, Xinze Li, Guizhen Chen, Wenhan Xia, Junjie Hu, Anh Tuan Luu, and Shafiq Joty. Data augmentation using LLMs: Data perspectives, learning paradigms and challenges. _arXiv preprint arXiv:2403.02990_ , 2024. 

- Guanting Dong, Hongyi Yuan, Keming Lu, Chengpeng Li, Mingfeng Xue, Dayiheng Liu, Wei Wang, Zheng Yuan, Chang Zhou, and Jingren Zhou. How abilities in large language models are affected by supervised fine-tuning data composition. _arXiv preprint arXiv:2310.05492_ , 2023. 

- Abhimanyu Dubey et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. URL `https://arxiv.org/abs/2407.21783` . 

- Dongdong Ge, Qi Huangfu, Zizhuo Wang, Jian Wu, and Yinyu Ye. Cardinal Optimizer (COPT) user guide. https://guide.coap.online/copt/en-doc, 2022. 

- Joren Gijsbrechts, Robert N Boute, Jan A Van Mieghem, and Dennis J Zhang. Can deep reinforcement learning improve inventory management? performance on lost sales, dual-sourcing, and multi-echelon problems. _Manufacturing & Service Operations Management_ , 24(3):1349–1368, 2022. 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- Mittelmann Hans. Benchmark for optimization software. _http://plato. asu. edu/bench. html_ , 2002. 

- R.V. Hogg, A.T. Craig, and J.W. McKean. _Introduction to Mathematical Statistics_ . Pearson, 8th edition, 2019. ISBN 9780134686998. 

- Ken Huang, Yang Wang, Feng Zhu, Xi Chen, and Chunxiao Xing. _Beyond AI: ChatGPT, Web3, and The Business Landscape of Tomorrow_ . Springer, 2024a. 

- Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao, and Benyou Wang. MAMO: A mathematical modeling benchmark with solvers. _arXiv preprint_ , 2024b. 

- INFORMS. 2013 Franz Edelman finalists, 2013. URL `https://www.informs.org/content/download/ 279469/2673366/file/2013edelman_finalWEB.pdf` . 

- Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. Mistral 7b. _ArXiv preprint_ , abs/2310.06825, 2023. URL `https://arxiv.org/abs/2310.06825` . 

- Bowen Jiang, Yangxinyu Xie, Zhuoqun Hao, Xiaomeng Wang, Tanwi Mallick, Weijie J Su, Camillo J Taylor, and Dan Roth. A peek into token bias: Large language models are not yet genuine reasoners. _arXiv preprint arXiv:2406.11050_ , 2024. 

- Nickvash Kani and Neeraj Gangwar. Tagged input and decode all-at-once strategy. `https://github.com/ MLPgroup/nl4opt-generation` , 2022. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

37 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ , 2020. 

- Elias Khalil, Hanjun Dai, Yuyu Zhang, Bistra Dilkina, and Le Song. Learning combinatorial optimization algorithms over graphs. _Advances in Neural Information Processing Systems_ , 30, 2017. 

- Junghwan Lee, Chen Xu, and Yao Xie. Transformer conformal prediction for time series. _arXiv preprint arXiv:2406.05332_ , 2024. 

- Beibin Li, Konstantina Mellou, Bo Zhang, Jeevan Pathuri, and Ishai Menache. Large language models for supply chain optimization. _arXiv preprint arXiv:2307.03875_ , 2023a. 

- Qingyang Li, Lele Zhang, and Vicky Mak-Hau. Synthesizing mixed-integer linear programming models from natural language descriptions. _arXiv preprint arXiv:2311.15271_ , 2023b. 

- Zhishuai Liu, Jesse Clifton, Eric B Laber, John Drake, and Ethan X Fang. Deep spatial Q-learning for infectious disease control. _Journal of Agricultural, Biological and Environmental Statistics_ , 28(4):749–773, 2023. 

- Max Marion, Ahmet Üstün, Luiza Pozzobon, Alex Wang, Marzieh Fadaee, and Sara Hooker. When less is more: Investigating data pruning for pretraining llms at scale. _arXiv preprint arXiv:2309.04564_ , 2023. 

- Mistral AI. Frontier ai in your hands - mistral nemo. _Mistral AI News_ , 2024. URL `https://mistral.ai/ news/mistral-nemo/` . 

- Vinod Nair, Sergey Bartunov, Felix Gimeno, Ingrid Von Glehn, Pawel Lichocki, Ivan Lobov, Brendan O’Donoghue, Nicolas Sonnerat, Christian Tjandraatmadja, Pengming Wang, et al. Solving mixed integer programs using neural networks. _arXiv preprint arXiv:2012.13349_ , 2020. 

- OpenAI. Openai o1 technical report. _OpenAI Technical Reports_ , 2024. Available at `https://openai.com/ research/o1-technical-report` . 

- RL Ott and Michael Longnecker. _An introduction to statistical methods and data analysis_ . Cengage Learning Inc., 2010. 

- Axel Parmentier. Learning to approximate industrial problems by operations research classic problems. _Operations Research_ , 70(1):606–623, 2022. 

- Tomasz P Pawlak and Krzysztof Krawiec. Automatic synthesis of constraints from examples using mixed integer linear programming. _European Journal of Operational Research_ , 261(3):1141–1157, 2017. 

- Tomasz P Pawlak and Michael O’Neill. Grammatical evolution for constraint synthesis for mixed-integer linear programming. _Swarm and Evolutionary Computation_ , 64:100896, 2021. 

- Ganesh Prasath and Shirish Karande. Synthesis of mathematical programs from natural language specifications. _arXiv preprint arXiv:2304.03287_ , 2023. 

- Meng Qi, Yuanyuan Shi, Yongzhi Qi, Chenxin Ma, Rong Yuan, Di Wu, and Zuo-Jun Shen. A practical end-to-end inventory management model with deep learning. _Management Science_ , 69(2):759–773, 2023. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

38 

- Hengle Qin, Jun Xiao, Dongdong Ge, Linwei Xin, Jianjun Gao, Simai He, Haodong Hu, and John Gunnar Carlsson. Jd. com: Operations research algorithms drive intelligent warehouse robots to work. _INFORMS Journal on Applied Analytics_ , 52(1):42–55, 2022. 

- Qwen Team. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2024. URL `https://arxiv.org/ abs/2407.10671` . 

- Rindra Ramamonjison, Haley Li, Timothy T. L. Yu, Shiqi He, Vishnu Rengan, Amin Banitalebi-Dehkordi, Zirui Zhou, and Yong Zhang. Augmenting operations research with auto-formulation of optimization models from problem descriptions. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: EMNLP 2022 - Industry Track_ , pages 29–62, 2022. 

- Rindranirina Ramamonjison, Timothy Yu, Raymond Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar, Shiqi He, Mahdi Mostajabdaveh, Amin Banitalebi-Dehkordi, Zirui Zhou, et al. NL4Opt competition: Formulating optimization problems based on their natural language descriptions. In _NeurIPS 2022 Competition Track_ , pages 189–203. PMLR, 2023. 

- Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, YK Li, Y Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- Samuel Sanford Shapiro and Martin B Wilk. An analysis of variance test for normality (complete samples). _Biometrika_ , 52(3-4):591–611, 1965. 

- Noah Shinn, Beck Labash, and Ashwin Gopinath. Reflexion: An autonomous agent with dynamic memory and self-reflection. _arXiv preprint arXiv:2303.11366_ , 2023. 

- Daniel Sroka and Tomasz P. Pawlak. One-class constraint acquisition with local search. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , 2018. 

- Richard S Sutton and Andrew G Barto. _Reinforcement Learning: An Introduction_ . MIT press, Cambridge, MA, USA, 2nd edition, 2018. 

- Zhengyang Tang, Xingxing Zhang, Benyou Wan, and Furu Wei. Mathscale: Scaling instruction tuning for mathematical reasoning. _arXiv preprint arXiv:2403.02884_ , 2024. 

- Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto. Stanford alpaca: An instruction-following Llama model. `https://github. com/tatsu-lab/stanford_alpaca` , 2023. 

- Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving olympiad geometry without human demonstrations. _Nature_ , 625(7995):476–482, 2024. 

- Hanzhao Wang, Zhongze Cai, Xiaocheng Li, and Kalyan Talluri. A neural network based choice model for assortment optimization. _arXiv preprint arXiv:2308.05617_ , 2023a. 

- Haochun Wang, Chi Liu, Nuwa Xi, Zewen Qiang, Sendong Zhao, Bing Qin, and Ting Liu. Huatuo: Tuning llama model with chinese medical knowledge. _arXiv preprint arXiv:2304.06975_ , 2023b. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

39 

- Mengxin Wang, Dennis J Zhang, and Heng Zhang. Large language models for market research: A dataaugmentation approach. _arXiv preprint arXiv:2412.19363_ , 2024. 

- Xiao-Jun Wang, Tao Liu, and Weiguo Fan. Tgvx: Dynamic personalized POI deep recommendation model. _INFORMS Journal on Computing_ , 35(4):786–796, 2023c. 

- Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A Smith, Daniel Khashabi, and Hannaneh Hajishirzi. Self-instruct: Aligning language models with self-generated instructions. _arXiv preprint arXiv:2212.10560_ , 2022. 

- Yizhong Wang, Hamish Ivison, Pradeep Dasigi, Jack Hessel, Tushar Khot, Khyathi Raghavi Chandu, David Wadden, Kelsey MacMillan, Noah A Smith, Iz Beltagy, et al. How far can camels go? Exploring the state of instruction tuning on open resources. _arXiv preprint arXiv:2306.04751_ , 2023d. 

- Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Jessica Wang, Xiongwei Han, Xiaojin Fu, Tao Zhong, Jia Zeng, Mingli Song, et al. Chain-of-experts: When LLMs meet complex operations research problems. In _The Twelfth International Conference on Learning Representations_ , 2023. 

- Lanling Xu, Junjie Zhang, Bingqian Li, Jinpeng Wang, Mingchen Cai, Wayne Xin Zhao, and Ji-Rong Wen. Prompting large language models for recommender systems: A comprehensive framework and empirical analysis. _arXiv preprint arXiv:2401.04997_ , 2024. 

- Wojciech Zaremba, Greg Brockman, and Others. OpenAI codex. _OpenAI Blog_ , 2021. URL `https://openai. com/blog/openai-codex/` . 

- Zihan Zhang, Yuan Zhou, and Xiangyang Ji. Model-free reinforcement learning: From clipped pseudo-regret to sample complexity. In _International Conference on Machine Learning_ , pages 12653–12662. PMLR, 2021. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

1 

## **ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling Online Supplement** 

#### **Appendix A: Appendix** 

#### **A.1. Criteria for Difficulty Level of Problem** 

We need to first highlight that the difficulty associated with optimization modeling is inherently challenging to quantify. Unlike solving optimization problems that can be assessed based on the number of variables, constraints, or model forms, the complexity of optimization modeling arises in enabling a large model to learn the mapping from natural language to optimized models. This difficulty primarily relates to the model’s reasoning abilities and its capacity for abstracting complex problem descriptions. 

Nevertheless, this study adopts a heuristic approach to assess the difficulty of modeling problems. We propose four evaluation criteria and provide illustrative examples of problem difficulty (see Appendix A.7). Using these criteria and specific examples, GPT-4 independently evaluates the difficulty level of each problem, ultimately categorizing them into three levels: easy, medium, and hard. The four criteria considered in this study are as follows: 

1. Problem size: This includes the number of constraints, objectives, and variables described in the natural language problem. Generally, the larger the problem, the higher the complexity of the model. (As shown in the statistical data in Figure 13, we sample 100 instances for each of the three difficulty levels from the training dataset. The average numbers of variables and constraints in these samples align with the proposed evaluation criteria.) 

2. Complex and logical relationships: The complexity of relationships between variables and the logical structure of objective functions and constraints significantly affect modeling difficulty. Problems involving intricate logical conditions, such as "if-else" statements, "or" conditions, and nonlinear functions, increase the challenge of formulating precise mathematical models. 

3. Ambiguity and complexity of natural language description: Natural language descriptions often contain ambiguous or polysemous expressions, which complicate the task of translating them into precisely defined mathematical models. Ambiguities in wording, implicit constraints, and unclear priorities require additional clarification and assumptions for accurate modeling. 

4. Requirement for interdisciplinary knowledge: Certain natural language problems may encompass specific domain knowledge (e.g., economics, engineering, biology), necessitating the application of expertise from these fields for accurate modeling. This requires not only operations research skills but also an interdisciplinary understanding, thereby increasing the complexity of the modeling process. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

2 

These four criteria collectively provide a comprehensive framework for evaluating the difficulty of translating natural language descriptions into mathematical models in operations research. 



<!-- Start of picture text -->
100<br>35 Average Variables Determined Parameters (%)<br>Average Constraints Undetermined Parameters (%)<br>30 80<br>25<br>60<br>20<br>15 40<br>10<br>20<br>5<br>0 0<br>Easy Medium Hard<br>Difficulty Levels<br>AverageCount (%)Proportion<br><!-- End of picture text -->

**Figure 13** This figure illustrates the statistical data obtained after sampling 100 problems for each of the three difficulty levels from the training dataset. First, the proportion of optimization problems with **determined parameters** is calculated and presented by the yellow line. For this type, the average number of constraints and variables is computed and visualized as a bar chart. For problems with **undetermined parameters** (parameters such as the number of warehouses can be manually designed, refer to example provided in Appendix A.7.3), only the proportion is calculated and represented by the red line. 

#### **A.2. Prompt Template for Expansion** 

#### **Description:** 

In the _Expansion_ phase, we design two prompts to enhance the effectiveness of the model. The first prompt aims to generate a sufficiently broad range of operations research scenarios and industries, serving as a reference for large language model to expand scenarios. The second prompt leverages the few-shot learning capability of the model, using three sample data points to generate a specific optimization problem within new operations research scenario. The new scenario is derived from the result produced by the first prompt. The term highlighted in the black box, <mark>select from the scenario list</mark> , in the second prompt refers to the process of randomly selecting a scenario from the output generated by the first prompt. 

#### **Scenario Generation Prompt:** 

```
Pleaselist100specificapplicationscenariosorindustrieswhereoptimizationmodelingareutilized.These
```

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

3 

```
scenariosshouldcoverdiversedomainssuchaslogisticsandsupplychainmanagement,manufacturing,energy
andenvironment,healthcare,transportation,financeandinsurance,agriculture,andmilitarydefense.Each
scenarioshouldbeasspecificaspossible,reflectingpracticalusesofoptimizationtechniques.Yourresults
shouldbestructuredsystematicallyandreturnedinJSONformat.
```

#### **Prompt for Expansion:** 

```
Imagineyouareaseasonedoperationsresearchalgorithmengineer.Yourtaskistodevelopanoperations
researchproblemthatiscloselyalignedwithreal-worldapplicationsandtoprovidethecorresponding
optimizationmodelalongwithCOPTsolvercode.Theproblemyoudesignshouldberelevanttotheselected
scenarioandalignwithitsspecificcharacteristics:selectfromthescenariolist.Pleasecarefullyfollow
theformatandstructureoftheexamplesprovidedbelowasareferencetocraftanewoptimizationmodeling
problem.
```

```
#Example1:
#Scenario#:
Retailing
```

```
#QuestionType#:
```

```
IntegerProgramming
```

```
#Problem#:
```

```
Aleathershoestoreemploys5full-timesalespersonsand4part-timesalespersons.Inordertooptimize
```

```
theworkingenvironmentandconsideremployeehealth,thestoredecidestolimittheovertimehoursofeach
full-timeemployee.Thefollowingtableshowstheworkinghoursandwageinformationfortheemployees:
```

- `| | Monthly Working Hours | Sales (pairs/hour) | Wage (dollars/hour) | Overtime Pay (dollars/hour) |` 

- `| :–-: | :–-: | :–-: | :–-: | :–-: |` 

- `| Full-time | 160 | 5 | 1 | 1.5 |` 

- `| Part-time | 80 | 2 | 0.6 | 0.7 |` 

```
Theprofitperpairofshoessoldis0.5dollars.Thestorehassetthefollowinggoals:
```

- _p_ 1 `: Achieve a monthly sales volume of at least 5500 pairs.` 

- _p_ 2 `: Limit the overtime hours of each full-time salesperson to no more than 20 hours.` 

- _p_ 3 `: Ensure full employment for all salespersons and give extra consideration to full-time employees.` 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

4 

- _p_ 4 `: Minimize overtime hours as much as possible.` 

```
Pleasedevelopanobjectiveprogrammingmodelforthisproblem.
```

```
#CompletionSolution#:
```

```
##MathematicalModel:
```

```
Toachievethegoalsoftheleathershoestore,wewilluseanobjectiveprogrammingmodeltobalancethe
achievementlevelsofeachgoal.Themodelisasfollows:
```

```
#Example2:
```

```
#Scenario#:
```

```
Agriculture
```

```
#QuestionType#:
```

```
Non-LinearProgramming
```

```
#Problem#:
```

```
Anagriculturalcompanywantstooptimizetheclimateconditionsinsidetheirgreenhousetoimprovethe
yieldandqualityofspecificcrops.Thecompanygrowstwomaincrops:tomatoesandcucumbers.Toachieve
theoptimalgrowthconditions,precisecontroloftemperature,humidity,andCO2concentrationinsidethe
greenhouseisrequired.Eachcrophasdifferentrequirementsfortheseenvironmentalfactors,andthecompany
wantstoadjustthegreenhouse’senvironmentalparameterstomeetthegrowthneedsofbothcropsandmaximize
thetotalyield.
```

```
#CompletionSolution#:
```

```
#MathematicalModel:
```

###### `### Decision Variables:` 

- _T_ `: Temperature inside the greenhouse (°C)` 

- _H_ `: Humidity inside the greenhouse (%)` 

- _C_ `: CO2 concentration inside the greenhouse (ppm)` 

```
...onemoreexample...
```

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

5 

```
#Example:
```

#### **A.3. Prompt Template for Augmentation** 

#### **Description:** 

In the following steps for _Augmentation_ , text highlighted by black boxes, such as Input ... , represents placeholders that need to be filled in during actual use as input for the large language model (e.g., GPT-4). Parentheses (You should provide ...) act as prompts, indicating that the model will generate improved output to be placed at the specified location. 

#### **A.3.1. Prompt Template for Altering Objective and Constraints** 

```
Imageyouareanoperationsresearchalgorithmengineer,Iwillprovideyouwithanentrycontainingaproblem
description,anoptimizationmodel,andCOPTcode.Yourtaskistomodifytheconstraintsorobjectivesin
theproblemdescriptionbasedontheactualsituationandaccordinglyadjustthecorrespondingmodelandcode.
Pleasefollowthestepsbelowforyouroutput:
```

`1. Real-World Scenario Consideration:` 

```
Basedontheproblemdescription,pleaseconsiderhowthisproblemwouldchangeinareal-worldscenario,
listingaspecificaswellasfeasiblechange.
```

`2. Modify Problem Description:` 

```
Consideringthevariationyoulistedinthepreviousstep,makechangestotheproblemdescription.
```

###### `3. Model and Code Modification:` 

```
Youareaskedtomodifytheoriginaloperationsresearchmodelbasedontheoriginaloperationsresearchmodel,
takingintoaccountthechangedproblemsituation,andmodifythecorrespondingCOPTcode.
```

`4. Complete Output:` 

```
Aftermodifyingthemodel,youshouldoutputthecompleteproblemdescription,mathematicalmodel,andCOPT
codeforthenewscenariointheoriginalformat.
```

```
Task:
```

```
Followthestepsoutlinedtoadapttheproblemforareal-worldscenario,andprovideacompletesolutionin
theoriginalformat.
```

```
OriginalEntry:
```

```
Inputtheoriginalentryhere
```

- `#Completion Solution#:` 

> `## Modified Problem Description:` 

```
Toaddressthereal-worldscenarioidentified,theproblemdescriptionhasbeenmodifiedasfollows:
```

```
(Youshouldprovidethemodifiedproblemdescriptionhere)
```

> `## Modified Mathematical Model:` 

```
Basedonthechangesinproblemscenario,themathematicalmodelhasbeenadaptedasfollows:
```

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

6 

```
(Youshouldprovidethemodifiedmathematicalmodelhere)
```

```
##ModifiedCOPTCode:
```

```
TheCOPTcodehasbeenupdatedtoreflectthechangesinthemathematicalmodel:
```

```
(YoushouldprovidethemodifiedCOPTcodehere)
```

#### **A.3.2. Prompt Template for Rephrasing Questions** 

###### `#Task#:` 

```
Imageyouareauserworkingwithalargelanguagemodel.Iwillprovideyouwithanentrycontaininga
problemdescription,anoptimizationmodel,andCOPTcode.Yourtaskistorephrasetheproblemdescription
usingyourownwording,ensuringthatyourexpressiondiffersinstylefromtheoriginal,whilepreservingthe
originalmeaning.Youshouldensurethatthemathematicalmodelremainsconsistentandvalidundertherevised
description.
```

```
Youroutputshouldreplacetheoriginalproblemdescriptionwithyourimprovedversion,leavingthe
optimizationmodelandCOPTcodecompletelyunchanged.Thefinaloutputmustretainthesameformatasthe
originalentry.Belowistheoriginalentry:
```

```
OriginalEntry:
```

```
Inputoriginalentryhere
```

```
#CompletionSolution#:
```

```
Therewrittenproblemdescriptionisasfollows:
```

```
(Youshouldprovidetherewrittenproblemdescriptionhere)
```

#### **A.3.3. Prompt Template for Incorporating Multiple Modeling Techniques** 

```
Task:
```

```
Imageyouareaseasonaloperationsresearchengineer,Iwillprovideyouwithanentrycontainingaproblem
description,anoptimizationmodel,andCOPTcode.Yourtaskistoreconstructtheoptimizationmodel,taking
intoaccountabroaderrangeofmodelingtechniques.
```

```
Followthefollowingstepstoenhancethemodelbyincorporatingmultiplemodelingtechniques.Provide
detailedexplanationsforeachmodificationandtherationalebehindselectingeachtechnique.
```

```
#Executionsteps#:
```

```
Incorporatemultiplemodelingtechniquesintotheprovidedmathematicalmodel.Followthesesteps:
```

`1. Techniques Instruction:` 

```
Thefollowingshowsthedifferentmodelingtechniquesandtheconditionsunderwhichtheyareapplied:
```

- `Auxiliary Variables: Suitable for simplifying complex relationships or non-linearities in the model.` 

- `Big M Method: Appropriate for models with conditional constraints within a linear programming framework.` 

- `Penalty Functions: Useful for converting hard constraints into an unconstrained optimization problem.` 

- `...` 

`2. Identify Modification Needs:` 

7 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

```
AnalyzetheoriginalmodelandidentifyareaswheremodificationscouldbeusedbasedonTechniques
Instruction.
```

```
3.ModifytheModel:
```

```
Applytheselectedtechnique(s)tomodifyeithertheobjectivefunctionortheconstraintsoftheoriginal
mathematicalmodel.
```

```
4.ModifytheCode:
```

```
Basedonthemodifiedmodel,thecorrespondingcodeismodifiedfollowingthecodeformatofCOPT.
```

```
5.Organizetheresults:
```

```
Organizetheproblemdescription,modifiedmodelandmodifiedcodestrictlyagainsttheformatoftheoriginal
problem.
```

```
OriginalEntry:
```

```
Inputtheoriginalentryhere
```

```
#CompletionSolution#:
##MathematicalModel:
Afterincorporatingadditionalmodelingtechniques,thereconstructedoptimizationmodelisasfollows:
```

```
(Youshouldprovidethemodifiedmodelhere)
```

```
##ModifiedCode:
```

```
Basedontheenhancedmathematicalmodel,thecorrespondingcodeinCOPTformatisprovidedbelow:
```

```
(Youshouldprovidethemodifiedcodehere)
```

#### **A.4. Alpaca-like Template for ORLMs Training** 

#### **Description:** 

The following template is used for training and testing the ORLM. When utilizing this template, users should replace the {Question} section with a natural language description of the optimization modeling problem. The ORLM will then return outputs in a standardized format. 

```
Belowisanoperationsresearchquestion.Buildamathematicalmodelandcorrespondingpythoncodeusing
```

```
‘coptpy‘thatappropriatelyaddressesthequestion.
```

```
#Question:
```

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

8 

```
{Question}
```

```
#Response:
```

#### **A.5. Detailed Results of Numerical Experiments** 

#### **A.5.1. Numerical Results for Different Question Types** 

**Table 12** Comparison of ORLM and GPT-4 on IndustryOR across different difficulty levels and question types. 

|**Method**|**fi**|**Difficulty**|**fi**||**Que**|**stion **|**Types**||
|---|---|---|---|---|---|---|---|---|
||Easy|Medium|Hard|LP|NLP|IP|MIP|Others|
|Standard-GPT-4|45.0%|17.5%|15.0%|33.3%|0.0%|38.7%|12.9%|0.0%|
|ORLM-LLaMA-3-8B|57.5%|20.0%|35.0%|36.1%|0.0%|61.2%|19.3%|0.0%|



#### **A.5.2. Scaling Law Numerical Results** 

**Table 13** Performance comparison with varying data sizes 

|**Base Model **|**Data Size**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR**</sup>|**Micro**<br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|LLaMA-3-8B|30,000|88.9%|81.4%|43.6%|25.0%|72.3%|59.8%|
|LLaMA-3-8B|25,000|86.5%|82.4%|40.3%|25.3%|71.7%|58.6%|
|LLaMA-3-8B|20,000|88.2%|82.5%|37.9%|23.0%|71.6%|57.9%|
|LLaMA-3-8B|10,000|87.8%|81.8%|35.9%|25.0%|70.9%|57.6%|
|LLaMA-3-8B|8,000|83.7%|80.4%|40.1%|30.0%|70.4%|58.6%|
|LLaMA-3-8B|6,000|83.3%|79.9%|38.9%|24.0%|69.3%|56.5%|
|LLaMA-3-8B|4,000|80.0%|82.2%|33.6%|24.0%|68.9%|55.0%|
|LLaMA-3-8B|2,000|81.2%|68.9%|26.1%|24.2%|60.9%|50.1%|



**Table 14** Model performance comparison with different model sizes 

|**Base Model **|**Model Size**|**NL4OPT **|<sup>**MAMO**</sup><br>**EasyLP**|**MAMO**<br>**ComplexLP **|<sup>**IndustryOR**</sup>|**Micro**<br>**Avg**|**Macro**<br>**Avg**|
|---|---|---|---|---|---|---|---|
|Qwen2.5|14B|90.2%|83.5%|48.3%|26.0%|74.5%|62.0%|
|Qwen2.5|7B|86.1%|85.2%|44.1%|25.0%|73.7%|60.1%|
|Qwen2.5|3B|83.2%|84.2%|36.5%|24.0%|71.1%|57.0%|
|Qwen2.5|1.5B|75.5%|82.5%|30.3%|18.0%|66.9%|51.6%|
|Qwen2.5|0.5B|63.6%|73.3%|16.1%|13.0%|56.6%|41.5%|



**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

9 

#### **A.6. Hypothesis Testing on the Effectiveness of ORLM** 

As stated in the main text, a total of 30 participants were recruited for the study, including 14 experts and 16 students. The specific groupings and corresponding experimental results are presented in Table 15. 

**Table 15** Statistical table of ORLM experimental participants’ data 

|||Group A|||Group B||
|---|---|---|---|---|---|---|
|Grou|||||||
|p|Index|Accuracy Rate (%)|Time(min)|Index|Accuracy Rate (%)|Time(min)|
||AE1|0_._86|149_._9|BE1|1_._00|49_._1|
||AE2|0_._71|157_._4|BE2|0_._86|65_._7|
||AE3|0_._86|166_._0|BE3|0_._86|39_._6|
|Expert|AE4|0_._71|172_._4|BE4|0_._86|51_._1|
||AE5|0_._57|151_._0|BE5|0_._86|57_._1|
||AE6|0_._71|155_._4|BE6|1_._00|48_._7|
||AE7|0_._57|170_._2|BE7|0_._86|60_._4|
||AS1|0_._57|224_._3|BS1|0_._71|87_._0|
||AS2|0_._71|230_._7|BS2|0_._86|88_._1|
||AS3|0_._43|217_._3|BS3|0_._71|103_._2|
|Stdt|AS4|0_._71|222_._4|BS4|0_._86|94_._1|
|uen|AS5|0_._57|194_._5|BS5|0_._71|83_._7|
||AS6|0_._29|238_._7|BS6|0_._71|74_._7|
||AS7|0_._71|228_._0|BS7|0_._86|61_._6|
||AS8|0_._57|206_._4|BS8|0_._71|75_._4|



Our objective is to evaluate whether the use of the ORLM tool leads to significant improvements in both time efficiency and accuracy for students and experts, respectively. Accordingly, we formulate the null and alternative hypotheses as follows: 

- _Null Hypothesis H_ 0: There is **no significant difference** in the population means of the experimental data for experts (or students) before and after using the ORLM tool. 

- _Alternative Hypothesis H_ 1: There is a **significant difference** in the population means of the experimental data for experts (or students) before and after using the ORLM tool. 

Next, we conduct statistical tests separately for experts and students on both accuracy and time efficiency data. Before performing hypothesis testing, we first examine the distributional properties of the data to determine the most appropriate testing method. Specifically, we assess whether the data follow a normal distribution and whether homogeneity of variance is satisfied. 

To test for normality, we employ the _Shapiro-Wilk test_ , as it is more sensitive for small sample sizes ( _n ≤_ 50) (Shapiro and Wilk 1965). Similarly, to assess the homogeneity of variance, we use the _Levene’s test_ , which is also suitable for small samples (Ott and Longnecker 2010). The results of these tests are summarized in Table 16. 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

10 

**Table 16** Shapiro-Wilk and Levene test results 

|Type|Test|Group||Shapi<br>|ro-Wilk<br>|Lev<br>|ene<br>|
|---|---|---|---|---|---|---|---|
|||||stat|_p_-value|stat|_p_-value|
|Total|Accuracy|<sup>Group </sup><br>Group|<sup>A </sup><br> B|<sup>0.900</sup><br> 0.801|0.098<br>0.003|1.464|0.236|
||Time|Group <br>Group|A <br> B|0.879<br> 0.962|0.045<br>0.737|11.066|0.002|
|Expert|Accuracy|<sup>Group </sup><br>Group|<sup>A </sup><br> B|<sup>0.857</sup><br> 0.600|0.143<br>0.000|1.203|0.294|
||Time|Group <br>Group|A <br> B|0.903<br> 0.975|0.350<br>0.931|0.103|0.754|
|Student|Accuracy|<sup>Group </sup><br>Group|<sup>A </sup><br> B|<sup>0.860</sup><br> 0.641|0.120<br>0.000|1.201|0.292|
||Time|Group <br>Group|A <br> B|0.951<br> 0.983|0.720<br>0.976|0.013|0.909|



Table 16 presents Shapiro-Wilk and Levene test results for two outcome measures — accuracy and time — across total, expert, and student samples comparing Group A and Group B. 

While the expert and student subgroups show normality in time data for both groups (with _p_ -values above 0 _._ 05), the total sample reveals marginal normality in Group A ( _p_ = 0 _._ 045) and significant heterogeneity of variance ( _p_ = 0 _._ 002). For accuracy, all samples (total, expert, and student) exhibit severe non-normality in Group B ( _p ≤_ 0 _._ 003), despite meeting variance homogeneity criteria ( _p >_ 0 _._ 05). Consequently: 

- Time: A Mann-Whitney U test is recommended for the total sample due to Group A’s marginal normality and variance heterogeneity, though independent _t_ -tests may still apply to expert/student subgroups. 

- Accuracy: A Mann-Whitney U test is used across all samples due to Group B’s consistent non-normality. 

We summarize the results in Table 17. 

Table 17 presents key statistical metrics, including the statistic value (Stat), the _p_ -value (p-value), the 95% confidence level of the difference (Confidence Interval), the effect size (Hedge’s g), and the statistical power (Stat Power). 

In addition to standard hypothesis testing results, we have further computed the effect size (Hedge’s g) and the statistical power to provide a more comprehensive evaluation of the robustness of our conclusions (Cohen 2013). Specifically, Hedge’s g is a standardized measure of mean difference between two groups, which is an improved version of Cohen’s d designed for small sample sizes. It is important to note that effect size is independent of sample size, making it a more objective indicator 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

11 

**Table 17** Statistical testing results 

|Type|Test|Method|||Statistic Testin|g||
|---|---|---|---|---|---|---|---|
||||Stat|_p_-value|Confidence Interval|Hedge’s g|Stat Power|
|Total|Accuracy|Mann-Whitney U test|192.00|0.001|(0.14, 0.24)|1.46|0.97|
||Time|Mann-Whitney U test|0.00|0.000|(-134.02, -112.35)|-4.43|1.00|
|Expert|Accuracy|Mann-Whitney U test|44.00|0.008|(0.10, 0.25)|1.81|0.87|
||Time|t-test|-22.50|0.000|(-117.61, -96.85)|-11.26|1.00|
|Student|<sup>Accuracy </sup>|<sup>Mann-Whitney U test</sup>|56.5|0.006|(0.14, 0.26)|1.56|0.82|
||<br>Time|t-test|-20.27|0.000|(-151.29, -122.34)|-9.58|1.00|



of the generalizability of our findings, even for small samples. Statistical power (Stat Power), on the other hand, represents the probability of correctly rejecting the null hypothesis — i.e., detecting a true effect when one exists. A high statistical power reduces the risk of Type II errors (failing to detect a real effect). 

As shown in Table 17, at a 95% confidence level, the use of ORLM significantly improves both solution time and accuracy across all populations (total, expert, and student samples). The confidence intervals suggest that, after implementing ORLM, accuracy improves by approximately 10%–25%. Additionally, the total time saved in solving optimization modeling problems is 1.8-2.2 hours, with experts saving approximately 1.5–2 hours and students saving around 2–2.5 hours. Additionally, the absolute value of Hedge’s g values exceed 1, demonstrating a substantial effect size and indicating a large difference between the experimental and control groups. Furthermore, the statistical power values all exceed 0.8, which is considered a strong threshold, ensuring a high probability of detecting a true effect and minimizing the risk of a Type II error. 

In conclusion, our findings provide compelling evidence that ORLM significantly enhances both accuracy and efficiency for both students and experts in solving operational research modeling problems. 

#### **A.7. Examples of Questions with Different Difficulty Levels** 

**A.7.1. Easy Example** A company sells custom scooters and bikes for customers. The profit per scooter is $200 and the profit per bike is $300. Each product requires time with the design team and engineering team. Each scooter needs 2 hours with the design team and 3 hours with the engineering team. Each bike needs 4 hours with the design team and 5 hours with the engineering team. Per month, there are 5000 hours available on the design team and 6000 hours available on the engineering team. How many of each should the company make per month to maximize profit? 

**A.7.2. Medium Example** We consider the following employee scheduling problem: A company needs to reassign 6 employees to complete the work over the next ten days. The daily workforce 

**Huang et al.:** _ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling_ 

12 

requirements and the availability of each employee for reassignment are known. Let _wj_ denote the number of employees required on day _j_ , and _αij_ indicate whether employee _i_ is available for reassignment on day _j_ . Furthermore, let _I_ represent the set of all employees and _J_ denote the set of working days. 

The objectives are twofold: (1) to ensure that each day’s workforce requirements are met as closely as possible, minimizing the number of unfulfilled positions; and (2) to balance the distribution of workdays among employees, minimizing disparities in their workloads. 

**A.7.3. Hard Example** The scheduling of hot coil transportation involves vehicle dispatch between warehouses and between warehouses and docks. Transportation tasks between warehouses are called _transfer tasks_ , while those between warehouses and docks are called _dock tasks_ . 

Before the start of each shift, schedulers need to assign vehicles to the existing steel coil transportation tasks, determine the execution time for each task, and ensure all tasks are assigned. Tasks have merging rules: tasks with the same starting and ending points can be executed by the same vehicle, but the total weight and the total number of steel coils must not exceed the vehicle’s limits. Vehicles do not pick up new tasks while en route; they can only pick up a new task after completing the current one. 

**Task Format:** Steel coil ID, steel coil weight, starting warehouse, destination warehouse (dock), ship ID, task priority 

1. Minimize the number of vehicles used 

2. Ensure that all tasks are completed as early as possible 

3. Prioritize tasks with high priority 

Constraints is listed as follows: 

1. Vehicles have an initial parking spot and must start from this spot when executing the first task of the shift 

2. The number of steel coils loaded on a vehicle must not exceed the vehicle’s limit 

3. The weight of steel coils loaded on a vehicle must not exceed the vehicle’s limit 

4. The vehicle’s transportation speed must be within the maximum and minimum speed limits 

5. Different ships at the same dock must be loaded sequentially; the next ship’s loading can only start after the previous ship’s loading is completed 

6. There is a limit to the number of vehicles simultaneously executing dock tasks 

7. There is a limit to the number of vehicles simultaneously executing transfer tasks 

8. The number of vehicles operating simultaneously in the warehouse area has an upper limit 

9. No new tasks should be assigned to vehicles in the last half hour of the current shift 

The sequence of tasks and estimated time nodes for all vehicles within this shift. 

