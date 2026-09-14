Deep Insights into Automated Optimization with Large Language Models and Evolutionary Algorithms 

He Yu<sup>a,b</sup> , Jing Liu<sup>a,b</sup> 

_aSchool of Artificial Intelligence, Xidian University, 2 South Taibai Road, Xi’an, 710071, Shaanxi, China bGuangzhou Institute of Technology, Xidian University, Knowledge City, Guangzhou, 510555, Guangdong, China_ 

# **Abstract** 

Designing optimization approaches, no matter heuristic or meta-heuristic, often require extensive manual intervention and struggle to generalize across diverse problem domains. The integration of Large Language Models (LLMs) and Evolutionary Algorithms (EAs) presents a promising new way to overcome these limitations to make optimization more automated, where LLMs function as dynamic agents capable of generating, refining, and interpreting optimization strategies, while EAs explore complex solution spaces efficiently through evolutionary operators. Since this synergy enables a more efficient and creative searching process, in this paper, we first conduct an extensive review of recent research on the application of LLMs in optimization, focusing on LLMs’ dual functionality as solution generators and algorithm designers. Then, we summarize the common and valuable design in existing work and propose a novel LLM-EA paradigm for automated optimization. Furthermore, focusing on this paradigm, we conduct an in-depth analysis on innovative methods for three key components, namely, individual representation, variation operators, and fitness evaluation, addressing challenges related to heuristic generation and solution exploration, particularly from the perspective of LLM prompts. Our systematic review and thorough analysis into the paradigm can help researchers better understand the current research and boost the development of combining LLMs with EAs for automated optimization. 

_Keywords:_ evolutionary algorithms, large language models, optimization, prompt engineering, deep learning 

# **1. Introduction** 

Optimization [1] plays a pivotal role in solving complex challenges across various industries, from logistics and manufacturing to machine learning and healthcare. At its core, optimization seeks to identify the best solution from a set of candidates according to specific objectives, while adhering to constraints. The growing scale and complexity of real-world optimization problems demand approaches that can navigate vast search spaces efficiently. Traditional optimization methods, such as gradient-based approaches and mathematical programming, have long been employed for problems with well-defined objective functions. However, these methods often struggle with real-world problems that are non-differentiable, multi-modal, or laden with constraints and uncertainties. This gap has driven the development of more flexible, adaptable, and scalable methods, leading to the rise of **heuristics** [2], which aim to provide approximate solutions efficiently. 

Heuristics emerged as practical tools for generating “good-enough” solutions without requiring exhaustive searches. While heuristics have been successful in many applications, they come with limitations. Traditional heuristics often require careful manual design, limiting their adaptability to new problems. **Meta-heuristics** [3, 4], such as genetic algorithms [5] and simulated annealing [6], offer more general approaches but often require parameter fine-tuning and expert knowledge. **Hyper-heuristics** [7, 8] attempt to automate the selection or generation of heuristics, representing a step forward. However, they remain constrained by predefined low-level heuristics or components, limiting their adaptability to highly dynamic and complex problems. 

The integration of **Large Language Models (LLMs)** [9] and **Evolutionary Algorithms (EAs)** [10] presents a promising new way to overcome these limitations. LLMs function as dynamic agents capable of generating, refining, and interpreting optimization strategies, while EAs explore complex solution spaces efficiently through evolutionary 

_Preprint submitted to arXiv_ 

_October 29, 2024_ 



Figure 1: The major development of heuristics 

operators like selection, mutation, and crossover. Together, **LLM-EA** offers the potential to reduce the need for manual tuning and expert knowledge, paving the way for more automated and adaptable optimization frameworks. 

This paper makes several key contributions to the study of integrating LLMs with EAs for automated optimization. First, we provide a brief review of the historical development of heuristics, from traditional methods to hyperheuristics, offering readers a foundational understanding of the field. Then, we conduct an extensive review of recent research on the application of LLMs in optimization, highlighting their roles as searching operators, solvers, and in algorithm design. Building on these insights, we summarize the common and valuable design in existing work and propose a novel **LLM-EA paradigm for automated optimization** , which combines the strengths of LLMs and EAs to enhance the efficiency and adaptability of optimization processes. Furthermore, focusing on the paradigm, we conduct an in-depth analysis on innovative methods for the three key components, namely, individual representation, variation operators, and fitness evaluation, addressing challenges related to heuristic generation and solution exploration. Finally, we identify current challenges and outline future directions for research, emphasizing the potential for further advancements in generalization, transparency, and scalability in LLM-EA systems. 

The remainder of this paper is organized as follows: Section 2 presents the evolution of heuristics in automated optimization, offering a detailed overview of traditional, meta-, and hyper-heuristic approaches. Section 3 explores the key technologies of LLMs and EAs that enable effective heuristic and solution generation. Section 4 discusses recent advancements in LLM-based optimization, followed by a detailed analysis of the novel LLM-EA automated optimization paradigm in Section 5. In Section 6, we identify and address the challenges associated with LLMEA systems and suggest future research directions to enhance their scalability and transparency. Finally, Section 7 concludes the paper with key insights and the potential impact of this research on future optimization methodologies. 

# **2. Evolution of Heuristics for Automated Optimization** 

Heuristics are problem-solving techniques designed to provide approximate solutions to optimization problems where finding the exact solution is computationally prohibitive. Throughout the evolution from heuristics to metaheuristics and hyper-heuristics as shown in Figure 1, the key goal is to create a more generalized, flexible, and automated approaches for solving optimization problems. Each development reduces the dependence on problemspecific adjustments and domain-specific expertise. In the following subsections, we briefly discuss each of these developments. 

# _2.1. Pre-Heuristic Approaches to Optimization_ 

Before the development of heuristics, optimization largely relied on methods such as exhaustive search, linear programming, and gradient-based techniques. While effective for small and well-structured problems, these methods struggled with the increasing size and complexity of modern optimization tasks. Exhaustive search, for example, systematically exploring all possible solutions quickly became computationally infeasible for combinatorial optimization problems like the Traveling Salesman Problem (TSP). 

2 

Traditional optimization techniques, such as mathematical programming and gradient-based methods, offered solutions for continuous variables and smooth objective functions but were insufficient for non-differentiable or discrete problems. These limitations spurred the need for more flexible and scalable approaches, which led to the rise of heuristic methods. 

# _2.2. Classical Heuristics_ 

The first wave of heuristics introduced simple yet practical techniques like _construction heuristics_ and _local search_ . **Construction heuristics** [11] build solutions incrementally, often making greedy decisions at each step. For example, the nearest-neighbor heuristic for the TSP selects the closest unvisited city at each step, offering quick but often suboptimal solutions. **Local search techniques** [12, 13, 14] start with an initial solution and attempt to improve it by making small adjustments within its neighborhood, such as the 2-opt heuristic [15] for the TSP, which swaps edges in a tour to reduce the distance. 

While these methods provided efficient ways to tackle complex problems, designing heuristics needs careful manual design, and also heuristics are easily trapped in local optima. These challenges highlighted the need for more robust strategies that could better balance exploration and exploitation in the searching process. 

# _2.3. Rise of Meta-Heuristics_ 

In response to the limitations of classical heuristics, **meta-heuristics** emerged as a more flexible and adaptable framework. Unlike classical heuristics, which are typically problem-specific, meta-heuristics are designed to be general algorithms applicable across a wide range of optimization problems, both combinatorial and continuous. 

A variety of meta-heuristic algorithms have been developed to tackle complex problems across various domains. Among them, EAs stand out as a prominent representative, like Genetic Algorithms (GAs) [5] , Memetic Algorithms [16], Particle Swarm Optimization (PSO) [17], Ant Colony Optimization (ACO) [18]. These algorithms share a common trait: they are designed to explore the solution space efficiently by leveraging principles inspired by natural processes or swarm intelligence. 

Despite their differences in specific implementations and searching operations, these meta-heuristic algorithms all embody a general framework that involves an iterative searching process. They initialize a set of candidate solutions, evaluate their quality based on a predefined objective function, and iteratively update the solutions through various mechanisms such as selection, crossover, mutation, or information sharing among individuals. This process allows them to escape local minima and explore diverse regions of the searching space, thereby increasing the likelihood of finding globally optimal solutions. 

However, despite their generalization capabilities, meta-heuristics still face key challenges, particularly their reliance on **carefully tuned parameters** and the need for **expert knowledge** . This dependence on domain knowledge for tasks like designing fitness functions, selecting appropriate operators (e.g., mutation and crossover), and adjusting algorithmic components reduces the true generality of meta-heuristics and limits their applicability across diverse optimization problems without significant manual intervention. 

# _2.4. Hyper-Heuristics: Automating Heuristic Design_ 

To reduce the reliance on expert knowledge and achieve more automated optimization, hyper-heuristic address problems by searching for and generating heuristics tailored to the problem. They operate at a more abstract level. Hyper-heuristics rely on predefined low-level heuristics, typically employing either _heuristic selection_ or _heuristic generation_ [7, 8, 19, 20], which output heuristics through various methods, including machine learning prediction or EA search. The machine learning approach is more generalized, relying heavily on extensive training data for prediction, while the EAs are based on an iterative search using specific problem-related training data. 

Despite hyper-heuristics’ potential to generalize across various problems, they are constrained by the quality and diversity of the available low-level heuristics or components, and if these components are not robust or flexible enough, the generated heuristics may perform poorly across different problems. Additionally, no matter the hyper-heuristics relying on training a prediction model or EAs, their effectiveness highly depends on the quality and quantity of training data. Poor or insufficient training data may result in suboptimal heuristics that fail to generalize effectively to unseen problem instances or variations. 

3 

# _2.5. Toward a New Era of Automated Optimization_ 

The integration of LLMs and EAs offers a promising new method for **automated optimization** , which leverages LLMs’ capabilities in generating combined with EAs’ iterative optimization techniques, resulting in a framework that can both solve optimization problems and design the optimization algorithms. The key innovations in this integration is the **dual-role** that LLMs play. 

First, LLMs can directly generate solutions by interpreting prompt content and applying searching operators such as mutation and crossover. In this capacity, LLMs function as **meta-heuristic agents** , dynamically producing solutions based on real-time feedback from the optimization process. Second, LLMs can generate and refine heuristics—problem-solving strategies, assuming the role of a **hyper-heuristic** . This allows for continuous adaptation and improvement of both the search strategies and the resulting solutions, enhancing the flexibility and effectiveness of the optimization process. 

The **LLM-EA automated optimization paradigm** holds the potential for generalized, scalable optimization across various domains, such as network design, logistics, and machine learning model optimization. By enabling the automated design of both solutions and the algorithms that generate them, this paradigm represents a significant leap forward in intelligent, adaptive problem solving, offering new opportunities for addressing complex, high-dimensional optimization challenges. 

# **3. Fundamental Technologies in LLM and EA for Automated Optimization** 

# _3.1. Overview of LLMs and EAs_ 

**Large Language Models** , such as GPT-4 and BERT [21], are built on the transformer architecture, which has revolutionized natural language processing (NLP). This architecture allows LLMs to process input sequences in parallel, rather than sequentially as seen in earlier models like RNNs [22] or LSTMs [23], making them significantly more efficient. The key innovation lies in the self-attention mechanism [24], which enables the model to weigh the importance of different words in a sentence relative to one another, regardless of their position in the text. This capability is crucial for understanding long-range dependencies in language and for capturing both syntactic and semantic information with high accuracy. The success of LLMs in NLP stems from pretraining on vast amounts of text, which allows them to generalize across various domains and tasks. By fine-tuning on specific tasks, LLMs can generate coherent and contextually relevant text, even in highly specialized fields. 

**Evolutionary Algorithms** , on the other hand, are inspired by the process of natural evolution and use mechanisms like **selection, mutation** , and **crossover** to solve optimization problems. EAs are particularly useful when the search space is large, complex, or non-differentiable, rendering traditional methods like gradient descent ineffective. EAs begin with an initial population of candidate solutions, which are evaluated using a fitness function to measure their performance. High-performing individuals are more likely to be selected for reproduction. The **crossover** operation combines features from two or more parent solutions to create offspring, while **mutation** introduces random variations to maintain diversity. This iterative process refines solutions over multiple generations, making EAs especially suitable for **black-box optimization** , where the internal structure of the system is unknown. 

# _3.2. Understanding Prompts in LLMs_ 

A **prompt** [25] is essentially the input provided to LLMs to guide its output. The purpose of a prompt is to specify what the LLMs should generate, whether it is answering a question, writing a paragraph, or completing a task based on a given example. A text prompt example is given in Figure 2(a). The simplicity or complexity of a prompt depends on the task at hand. At its core, a prompt can be thought of as the instruction or query that triggers the model’s response. This is a foundational component of using generative LLMs like GPT or BERT, as it sets the direction for the model’s output. 

# _3.2.1. Prompt techniques_ 

Prompt techniques refer to structured approaches for designing, formatting, and sequencing prompts to achieve optimal generative performance from LLMs. Common prompt techniques include: 

**Zero-Shot prompt** [26]: In this technique, LLMs are tasked with performing a job without presenting any examples. It solely depends on the directions stated in the prompt. As depicted in Figure 2(b), zero-shot prompt tests 

4 



Figure 2: The examples of prompting 

the LLMs’ capacity to comprehend and carry out the task solely based on the provided instructions, devoid of any supplementary context or samples. 

**Few-Shot prompt** [27]: As shown in Figure 2(c), this approach entails furnishing a handful of examples alongside the task directions to assist in guiding the model. These instances are commonly known as exemplars. By presenting the LLMs with a small number of pertinent cases, few-shot prompt can enhance its performance on the task by offering a clearer understanding of what is anticipated. 

**Chain-of-Thought prompt** [28]: This method encourages LLMs to dissect their reasoning process into consecutive steps before reaching the final answer. As illustrated in Figure 2(d), the Chain-of-Thought prompt can boost the model’s effectiveness on tasks that necessitate logical deduction or multi-step problem-solving. By prompting the model to articulate its thought process, this technique can make the model’s reasoning more transparent and accurate. 

# _3.2.2. Prompt optimization_ 

**Prompt optimization** [29, 30] refers to the process of refining prompts to enhance the generative performance of LLMs. It involves iteratively adjusting prompts, experimenting with different variations, and using automated techniques to optimize for accuracy, efficiency, and output relevance. The following principles are essential for effective prompt optimization: 

- **Prompt Ensembling** : This technique generates multiple variations of a prompt and aggregates their outputs to 

- improve response quality and diversity. 

- **Prompt Tuning** : Fine-tuning the structure, wording, and format of prompts can significantly impact the model’s 

- output quality, allowing for more targeted and precise results. 

- **Self-reflective Prompts** : In this iterative approach, the LLM evaluates its own responses, identifies potential 

- weaknesses, and suggests improvements, enabling continuous refinement. 

By applying these principles, prompt optimization can produce more reliable and fine-tuned outputs, pushing the capabilities of LLMs in complex problem-solving scenarios. 

# _3.3. EAs for Prompt Optimization_ 

EAs have been used to solve the optimization problem in LLMs, especially for optimizing the prompt. Prompts can be categorized into **continuous prompts** , which use numerical vectors (embedding vectors) to influence LLMs’ 

5 

behavior directly [31] and **text prompts** , which are natural language instructions. EAs can effectively optimize prompts by exploring different configurations and selecting the most effective ones. 

**Continuous prompts** involve tuning embedding vectors that act as "soft prompts", allowing fine control over the LLM’s responses. For example, _Black-Box Tuning_ (BBT) [32] applies EAs to optimize **continuous prompts** represented as embedding vectors, which iteratively adjusts these vectors to improve performance on various language tasks, such as sentiment analysis and question answering. BBT shows that continuous prompts can be fine-tuned using EAs even when the LLM is treated as a black-box system. 

For **text prompts** , EAs adjust phrasing and structure to find better ways of prompting the LLM. For example, _EvoPrompt_ [33] utilizes evolutionary operators like mutation and crossover to modify parts of prompts, enabling the exploration of new variations that might lead to better performance. _PromptBreeder_ [34] takes this further by evolving both the task-specific prompts and the evolutionary operator used to refine these prompts. This dual evolution ensures that the model not only generates high-quality prompts but also refines the method of prompt generation itself, ultimately leading to more robust outcomes when the LLM is later applied to complex optimization tasks. 

As can be seen, EAs can improve the quality of prompts which guide LLMs to generate better responses, which is a natural application of EAs. In fact, more creatively, EAs are combined with LLMs to solve optimization problems, which is the focus of this paper and introduced in the following sections. 

# **4. Development of LLM-based Optimization and LLM-EA Automated Optimization Paradigm** 

In this section, we first summarize existing work on LLM-based optimization, highlighting key techniques and common patterns. Based on these insights, we propose a novel paradigm where LLMs generate solutions and heuristics, while EAs iteratively refine them. This LLM-EA paradigm aims to automate and enhance optimization processes, reducing the need for manual intervention and improving adaptability across diverse problems. 

# _4.1. LLM-based Optimization_ 

LLMs, with their vast knowledge base and advanced natural language understanding, reasoning, and problemsolving capabilities, have garnered significant attention in the field of optimization. Research efforts in this area have primarily focused on two main directions: exploring the **searching abilities** of LLMs and using LLMs to **model optimization problems** . While the focus of this paper is on the former, for more details on the latter, readers can refer to [35, 36]. There has also been research into using the fundamental mechanism behind LLMs— **Transformer architecture** —to solve optimization problems, which is also outside the scope of this paper, and readers can refer to [37, 38, 39] for further details. 

Our focus is on how LLMs function as **searching operators** within optimization processes. Regardless of the type of problem being addressed, the majority of research has treated LLMs as searching operators, embedding them into iterative procedures or coupling them with **EAs** . Certainly, LLMs have also been employed in other stages of the optimization process, such as initialization, evaluation, and selection. However, the role of LLMs as searching operators remains the most valuable and complex to execute effectively. Therefore, in this section, we delve into how LLMs have been designed and used as searching operators. For a more general overview, refer to [40, 41]. 

As searching operators, LLMs have been applied to a variety of optimization problems, extending their reach from **prompt optimization** , as discussed above, to classical numerical and combinatorial optimization problems, and even to **automatic algorithm design** . In **prompt optimization** , optimization techniques have been used to improve the quality of prompts [31, 32, 42, 43, 44, 45]. In fact, many of these studies [31, 42, 43, 44] have already treated LLMs as searching operators to directly optimize prompts, given that text is the format LLMs naturally excel in. Recognizing that LLMs can optimize text, and that numerical values can also be treated as a form of text, researchers have begun exploring whether LLMs can solve classical optimization problems directly [46]. They applied LLMbased searching operators to **continuous numerical optimization** , **combinatorial optimization** , and more complex optimization problems [47, 48, 49]. In these cases, LLMs are designed to generate candidate solutions directly for the given problem, effectively functioning as solvers. 

However, as research advanced, it became apparent that while LLMs are exceptional at generating text, their ability to handle numerical optimization was somewhat limited [50]. On the other hand, LLMs have shown remarkable capabilities in **code generation** [51, 52], leading researchers to shift their focus towards guiding LLMs to design 

6 

optimization algorithms rather than directly solving optimization problems. In this approach, LLMs are tasked with designing either specific components of an algorithm or entire algorithms. These algorithm components or complete algorithms are expressed in natural language, pseudo-code, or real code. Given that LLMs are more proficient at handling code than numerical values, there has been growing interest in utilizing LLMs for **automated algorithm design** . 

Next, we focus on the work taking LLMs as a solver or for automated algorithm design, which not only represent the core focus of optimization in this field, but also analyze the key developments and technologies that have emerged. 

# _4.2. LLMs as a Solver_ 

Treating LLMs as a solver and asking them to generate solutions for optimization problems directly, the core technologies lie in designing prompts for LLM-based searching operators. In general, prompts contain two main types of information: the **problem details** and the **required output** from the LLM. In this case, the output is typically straightforward—producing one or more candidate solutions to the problem at hand. The real challenge arises in how the problem is presented to the LLM. The problem-related information in prompts can be categorized into three types: **available solutions** , **quality of those solutions** , and **guidance for the LLM’s search direction or pattern** . Most existing studies provide candidate solutions as examples, but the use of solution quality and search guidance varies across different works. Below, we summarize the major developments in this area. 

Initially, researchers simply provided LLMs with candidate solutions. A notable example of this is Meyerson et al.’s work [53], where LLMs were employed as crossover operators in EAs. By providing pairs of existing solutions, the LLMs generated new solutions based on these examples. No information about solution quality or search guidance was included in this work. Another early study is Lehman et al.’s work [54], where LLMs were designed as mutation operators in genetic programming (GP). Since GP deals with codes, the LLM-based mutation operators generated code solutions for the problems being tackled. Notably, this differs from later work on code generation for algorithm design. In [54], basic guidance was introduced alongside the solutions, with three LLM-mutation operators requiring the model to either: make changes or small changes to the current solution, or modify parameters of the current solution. While these instructions were simple, they introduced a level of search direction, influencing subsequent research. Hemberg _et al._ [55] applied LLMs to each part of GP, instead of just the mutation operator. 

As research advanced, it became evident that providing only candidate solutions was insufficient; including the **quality of solutions** helped LLMs learn how solutions differ. A representative work in this space is OPRO, proposed by Yang et al. [56], which provided objective function values alongside each solution, though no specific search guidance was offered. OPRO tested small-scale linear regression problems and TSPs, with a focus still on prompt optimization. Following OPRO, the inclusion of solution quality became a standard practice in LLM-based optimization. 

Further developments in the use of **searching guidance** emerged, recognizing its importance in steering LLMs more effectively. Following OPRO, Liu et al. [57] designed more detailed task instructions that were combined with EA steps. These instructions specified the sequence of operations, such as performing selection, followed by crossover, and then mutation. This combination of solution quality and structured guidance represented a significant step forward in prompt design. 

Beyond prompt design, researchers have also extended this LLM-driven optimization approach to more complex problems, such as **multi-objective optimization** [58, 59]. Additionally, several innovations have further refined this paradigm. For example, Lange et al. [60] applied **evolution strategies** , asking LLMs to generate the next mean for a desired fitness level. Brahmachary et al. [61] introduced a technique that split the population into two groups for **exploration** and **exploitation** , providing different search guidance for each group. Huang et al. [50] conducted a comprehensive comparative study on the ability of LLMs to generate solutions for optimization problems directly, offering insights into their relative strengths and limitations. 

# _4.3. LLMs for Automated Algorithm Design_ 

The use of LLMs to automate algorithm design has progressed significantly over recent years. Initially, researchers focused on a single-round process, where LLMs were prompted to design new meta-heuristics. In these early studies, LLMs typically selected and analyzed existing algorithms, generating new ones in pseudo-code format. However, the performance of these generated algorithms could not be evaluated online, and their application was limited to 

7 

conversational interactions rather than fully leveraging LLMs’ optimization potential [62, 63, 64]. We think these types of work are more like chatting with LLMs rather than mining the optimization ability of LLMs. 

A more advanced approach involves embedding LLM-based searching operators into an iterative process, allowing continuous improvement of the generated algorithms. This shift enabled LLMs to move beyond simple heuristic generation to creating meta-heuristics. Within this context, researchers have focused on generating both components of heuristics/meta-heuristics and complete algorithms. Various optimization problems have been explored, including numerical optimization, combinatorial optimization, multi-objective optimization, and even complex network optimization [47, 49]. Given the varying complexities of these problems, numerical and combinatorial optimizations have received the most attention, with subsequent studies expanding to multi-objective and complex problems. 

The type of algorithm generated and the problem used to test is not strictly one-to-one; some studies apply a single generated heuristic or meta-heuristic across multiple problem types. The iterative nature of algorithm improvement stems from two factors: LLMs’ ability to generate codes and the integration of an iterative process. One of the most widely used iterative processes is the EAs. 

Currently, the primary focus is on designing components within heuristics or meta-heuristics. Typically, an existing optimization algorithm is fixed, and LLMs are tasked with generating specific functions for the algorithm. For example, in **FunSearch** [65], LLMs generate functions to evaluate the score of each bin in the bin-packing problem. The prompt provides existing code, and the LLM is asked to generate only the function code. Similarly, **EoH** [66, 67, 68] uses both code and descriptions about the algorithm to generate new function components. EoH employs a guided local search (GLS) algorithm [14, 69], and the LLM generates an evaluation function embedded in GLS. However, the search guidance in EoH remains fixed throughout the iterative process. 

Recent advancements have introduced dynamic search guidance during the iteration process. Ye et al. [70] proposed a system with two LLMs: one for generation and one for reflection. The reflection LLM analyzes shortterm and long-term search results and provides updated search guidance to the generation LLM. Similarly, Sun et al. [71] developed a system of three LLM-based agents—Advisor, Coder, and Evaluator—that work together to analyze solutions and guide further searches, representing early steps toward LLMs guiding other LLMs. 

In addition to generating components for heuristics, LLMs have been applied to meta-heuristic component design. Huang et al. [72] used LLM-based crossover and mutation operators for multi-objective optimization. Huang et al. [73] extended this work to evolutionary multitasking algorithms, where LLMs were tasked with designing knowledge transfer models. In other studies, LLMs have been employed to design surrogate models for expensive optimization tasks [74] and learning rate schedules in evolutionary strategies [75, 76]. 

Designing complete heuristics or meta-heuristics is more challenging than just designing components, and research in this area remains limited. Yu et al. [49] proposed a method for generating complete heuristics to improve the robustness of complex networks [77, 78]. Stein et al. [79] developed a method for generating meta-heuristics for continuous optimization problems. This direction needs further study since we are more interested in letting LLMs design complete algorithms automatically. 

Although LLMs have been used to solve various optimization problems and design optimization algorithms, this research direction is just at the beginning, and most work just uses small-scale problems to validate the ability of LLMs in optimization. Undeniably, LLMs combined with EAs provide a promising new way for automated optimization. Thus, we summarize the common and most valuable design in existing work and propose a general LLM-EA automated optimization paradigm in the following subsection, which can help researchers better understand the current research and guide future research. 

# _4.4. LLM-EA Automated Optimization Paradigm_ 

Through the above review, we can see, that to enhance LLMs’ capabilities in solving optimization problems, researchers have increasingly integrated EAs with LLMs. This synergy enables a more efficient and creative searching process, with LLMs generating high-quality candidates and EAs optimizing these candidates through iterative refinement. This complementary relationship strengthens the continuous creativity, allowing for more automated optimization algorithm design. Building on this foundation, we propose an LLM-EA automated optimization paradigm in which LLMs and EAs work together to generate both _solutions_ and _heuristics_ , providing a flexible and powerful framework for automated optimization. Next, we first introduce each component of this paradigm and then present the whole paradigm. 

8 

Optimization problems aim to find the optimal candidate _x_<sup>∗</sup> that maximizes (or minimizes) a objective function _f_ ( _x_ ). For _solution search_ , the objective is to find _x_<sup>∗</sup> whose fitness is maximum, where _x_ ∈ _S_ solution, and _S_ solution is solution searching space : 



For _heuristic search_ , the objective is to find the best heuristic _x_<sup>∗</sup> for the optimization problem under consideration. The performance of _x_<sup>∗</sup> is evaluated on a training set _D_ = { _d_ 1, _d_ 2, . . . , _dk_ } of problem instances by aggregating as follows: 



where _S_ heuristic is heuristic searching space and A(.) is an aggregation function (e.g., average or weighted sum) used to combine the fitness values across instances. 

In the evolutionary process, at generation _t_ , the population consists of _N_ candidates: 



Each candidate in the population represents either a solution or a heuristic. 

In the paradigm, the evolutionary process includes three primary operators: selection, variation, and reflective. 

- **Selection Operator** : The selection operator _O_ select selects the candidates for conducting the variation operator based on their fitness values: 



ensuring that candidates with higher fitness are more likely to contribute to the next generation. 

- **Variation Operator** : The variation operator generates new individuals based on _P_ parent( _t_ ). One or more variation operators can be designed with different focus on exploration or exploitation. LLMs play a role in this process by generating offspring through prompt Pvariation : 

where Pvariation is defined as: 



- Here, Dproblem is the problem description, Dtask is the task instruction, which includes the variation logic, and _xi_ , . . . , _x j_ are the candidates as example data. 

- **Reflective Operator** : An optional reflective mechanism adjusts variation operators dynamically. The LLM refines the variation strategies based on the performance of previous generations: 



The LLM, acting as a searching operator, is guided by prompts. Whether variation prompts or reflective prompts are used, they share a common pattern that includes a _problem description_ , _task instructions_ , and _example data_ . The problem description refers to the detailed explanation or context of the problem that needs to be solved. The task instructions are the explicit directives given to the LLM, specifying the task or objective that the model needs to accomplish. The example data refers to real examples provided as input or reference, helping the LLM understand the task requirements or expected output format. 

For **variation prompts** , the _problem description_ outlines the optimization problem to be addressed. The _task instructions_ can vary from simple requirements to detailed variation logic, specifying how the LLM should approach generating. The _example data_ consists of previously evaluated candidates with fitness scores, guiding the LLM in creating improved solutions or heuristics according to the task instructions. An example of a variation prompt is present in Figure 3(a). 

In **reflective prompts** , the _problem description_ shifts to optimizing the existing task instruction of the variation prompt, focusing on improving the current prompt itself. The _task instructions_ then guides how to analyze and 

9 



Figure 3: (a) This is the variation prompt for the TSP. The problem description introduces the TSP and presents data for an instance of the problem. The example data provides several routes along with their respective lengths. The task instruction specifies the requirement to provide a route that is shorter than all the routes given in the example data. (b) This reflective prompt is aimed at refining or optimizing the task instruction for the TSP. 

**Algorithm 1** LLM-EA for Automated Optimization **Input:** Fitness function _fs_ or _fh_ , Number of generations _T_ **Output:** Best candidate found _x_<sup>∗</sup> 1: Initialize population _P_ (1) = { _x_ 1, _x_ 2, . . . , _xN_ }, where _xi_ ∈ _S solution_ / _S heuristic_ , _i_ = 1, 2, . . . , _N_ 2: **for** each candidate _xi_ in _P_ (1) **do** 

- 3: **if** Solution Search **then** 

- 4: Evaluate the fitness using _fs_ ( _xi_ ) 

- 5: **else if** Heuristic Search **then** 

- 6: Evaluate the fitness using the aggregation across training set: 

   - _f_ ( _xi_ ) = A ({ _fh_ ( _xi_ , _d_ 1), _fh_ ( _xi_ , _d_ 2), . . . , _fh_ ( _xi_ , _dk_ )}) 

- 7: **end if** 8: **end for** 9: **for** _t_ = 1 to _T_ **do** 

- 10: Apply the selection operator to form the parent population _P_ parent( _t_ ) using Eq. (4) 11: **for** each group candidates ( _xi_ , . . . , _x j_ ) in _P_ parent( _t_ ) **do** 12: Generate prompt Pvariation = {Dproblem, Dtask, _xi_ , . . . , _x j_ } 13: Apply the variation operator using Eq. (5) to obtain _P_ offspring( _t_ ) 14: **end for** 15: Evaluate the fitness of individuals in _P_ offspring( _t_ ) 16: Survivor selection to obtain population _P_ ( _t_ + 1) with _P_ offspring( _t_ ) and _P_ parent( _t_ ) 

- 17: **Optional:** Apply the reflective operator to refine variation operators by using Eq. (7) 18: **end for** 

- 19: **Return** best candidate _x_<sup>∗</sup> 

10 

compare the available _example data_ to generate new task instructions for the variation prompt. These _example data_ can either consist of macro-level statistical information, representing the overall characteristics of multiple candidates, or specific, feature-rich candidates or existing variation prompts. This example data serves as a reference for the LLM to generate more optimized instructions. An example of a reflective prompt is presented in Figure 3(b). 

**Explanation of the paradigm** : Algorithm 1 gives the detail of LLM-EA automated optimization paradigm. It begins by initializing a population of candidates and iteratively evaluates their fitness. Selection, variation operations are applied, where the LLM generates new candidates based on prompts. An optional reflective mechanism adjusts the variation operators based on feedback from previous generations, enhancing the optimization process over time. The algorithm continues for a set number of generations, ultimately returning the best candidate. 

# **5. In-Depth Analysis of Key Modules in LLM-EA Automated Optimization Paradigm** 

Building on the LLM-EA automated optimization paradigm, this section conducts a comprehensive analysis from two perspectives: prompt engineering for LLMs and the evolutionary process for iterative search. By integrating these two aspects, we provide a multidimensional exploration of the LLM-EA automated optimization paradigm. 

Prompts play a fundamental role in this paradigm by guiding LLMs through optimization tasks. The structure of these prompts—consisting of problem descriptions, task instructions, and example data—determines how effectively the LLM participates in tasks such as crossover, mutation, and reflective optimization. Prompts not only provide the LLM with the necessary reference points for generating new candidates, but also are embedded the logic of evolutionary operators, ensuring smooth integration with the optimization process. 

In the evolutionary process, we focus on three critical components: **individual representation** [80, 81], **variation operators** [82], and **fitness evaluation** [83, 84]. Individual representation shapes how candidates are structured and determine the searching space. Variation operators, such as mutation and crossover, guide the exploration of the searching space. Fitness evaluation drives the process by measuring how well the generated candidates meet the optimization objectives. 

The following subsections provide detailed explanations of how these components are systematically integrated into the prompt, ensuring that the LLM maximizes its effectiveness in the optimization task. Our analysis reveals how prompts dynamically influence each phase of the evolutionary process, offering deeper insights into the synergistic relationship between LLMs and EAs in automated optimization. 

# _5.1. Individual Representation for Heuristic_ 

Historically, the representation of solutions in optimization has been purely numerical, particularly in the case of continuous and combinatorial optimization problems, where candidates are expressed as vectors or arrays. While this method remains effective for many tasks, the advent of LLMs introduces new possibilities for representing heuristics. These representations expand beyond simple numerical encoding to incorporate natural language, pseudo-code, and even executable code. This shift allows LLMs to play a more creative role in generating novel problem-solving strategies. 

After analyzing current research, we define a novel classification of heuristic representation that extends traditional solution encoding and differentiates between three main types of heuristic representation: **Code-Centric Representation** , **Hybrid Representation** , and **Augmented Representation** , each tailored to different levels of complexity in optimization problems. 

- **Code-Centric Representation** : In this form, the heuristic is represented solely as executable code. For instance, FunSearch [65] uses LLMs to generate small, self-contained code snippets that are directly applied to optimization problems. The LLM evolves the code itself, which is designed to perform specific tasks or calculations without the need for external explanations. While this approach is computationally efficient, it lacks interpretability, as the generated code does not come with any accompanying documentation or reasoning. This method is better suited for well-defined problems where efficiency is prioritized over transparency. 

- **Hybrid Representation** : This method blends code with natural language descriptions. In the EoH [66] framework, LLMs not only generate executable code but also provide a natural language explanation of the code’s 

11 



Figure 4: An individual representation of EoH [66] is provided, where the heuristic is expressed in both natural language and executable code. The natural language description explains how the heuristic calculates scores for each bin, considering factors such as remaining capacity, bin index, and penalties for large differences. The code snippet implements this logic. A fitness score of 0.0143 reflects the performance of the generated heuristic in the optimization task. 

logic and intended purpose, as illustrated in Figure 4. This combination bridges the gap between machinegenerated heuristics and human-readable explanations. By co-evolving code and descriptions, this approach enhances both performance and interpretability, making it suitable for more complex tasks where understanding the reasoning behind the code is crucial. 

- **Augmented Representation:** This extends beyond previous representations by incorporating **executable code** , **natural language descriptions** , and **domain-specific expert knowledge** into the individual representation. For example, unlike FunSearch and EoH, which represent code snippets or code paired with explanations, AutoRNet [49] enhances the representation by embedding higher-level concepts from network science, such as **high-degree nodes** , **low-degree nodes** , **critical nodes** , and **network connectivity** . This enriched representation allows the LLM to contextualize the code within a broader domain-specific framework, facilitating a deeper understanding of the problem. By incorporating expert knowledge, the LLM is not merely working with logic and procedures but is equipped with the conceptual background to generate more advanced and applicable algorithms. **Augmented Representation** ensures that the generated heuristics can address complex optimization problems with a higher degree of relevance and adaptability. 

# _5.2. LLM-based Variation Operators_ 

Traditional EAs rely on predefined operators such as mutation and crossover, which require detailed step-bystep programming and domain-specific expertise. With the advent of LLMs, the role of these operators has evolved, enabling more flexible and dynamic approaches to solution generation and heuristic manipulation. We identify three key advantages that LLMs bring to EAs: 

1. **High-Level Instructions Remove the Need for Step-by-Step Programming** . Traditionally, variation operators require precise, step-by-step programming to define how solutions are selected, combined, and modified. 

12 



Figure 5: (a) An example of the constructed prompt when utilizing LMEA to solve TSPs. The evolutionary operator is presented as a natural language in task instructions. (b) An prompt of EoH uses the E2 strategy to design a new heuristic. 

LLMs eliminate this need by interpreting high-level task instructions written in natural language, enabling flexible solution generation. For instance, the LMEA [57] framework is illustrated in Figure 5(a), where LLMs are given general directives for tasks like parent selection and mutation, allowing them to autonomously generate solutions based on these instructions without needing detailed programming. This approach reduces reliance on domain-specific expertise and enables more flexible solution exploration. 

2. **Advanced Manipulation of Heuristics via Natural Language** . Heuristics, unlike numerical solutions, are complex algorithms or pieces of code. LLMs excel in applying variation operators to these heuristics by using their natural language understanding to combine, refine, and adjust logical structures. For example, in the **EoH** [66] framework, five prompt strategies ( **E1, E2, E3, M1, and M2** ) are designed and categorized into two groups: **Exploration** and **Modification** . Each strategy uses prompts to guide the LLM with different emphases in evolving heuristics based on current population performance and heuristic structure. For example, the detail of **E2** strategy is shown in Figure 5(b), which put emphasis on designing a new heuristic different from the given ones. 

3. **Incorporation of Domain-Specific Knowledge into Variation Operators** : A significant advantage of LLMbased variation operators is their ability to integrate expert domain knowledge into the evolutionary process, as demonstrated in **AutoRNet** [49] through its **Network Optimization Strategies (NOS)** . By embedding specialized knowledge from fields like network science (e.g., degree distribution, path characteristics, clustering coefficient, centrality measures, and community structure) into the variation operations, LLMs can guide mutation and crossover with insights specific to the problem domain. This allows for more sophisticated and effective heuristics that address complex, domain-specific optimization challenges. For example, in network optimization, AutoRNet uses domain knowledge to adaptively modify network structures, ensuring that the generated heuristics are deeply informed by network science principles. This integration of expert knowledge allows LLMs to generate heuristics that are not only generalizable but also highly specialized, providing a new 

13 

# layer of flexibility and precision in the evolutionary process. 

Beyond generating solutions or heuristics, LLMs also play a pivotal role in optimizing the variation operators themselves. ReEvo [70] introduces a novel reflective mechanism where LLMs evaluate and refine the variation operators by analyzing the performance of previously generated heuristics. Unlike traditional EAs that rely on static operators, ReEvo enables LLMs to reflect on both short-term and long-term performance data. This allows the LLMs to generate adaptive mutation and crossover strategies, leading to more effective exploration of the search space. 

- **Short-term Reflection** : LLMs assess the recent individuals, identifying immediate changes needed in mutation or crossover operations. This dynamic response helps the evolutionary process adapt quickly to the promising searching direction. 

- **Long-term Reflection** : LLMs evaluate broader trends in the performance of heuristics over multiple generations, allowing for deeper adjustments to the evolutionary strategy. This ensures that the operators evolve alongside the heuristics, leading to more robust solutions. 

This reflective feedback loops enables LLM-driven optimization of the search strategy itself, moving beyond simple heuristic generation to a more dynamic, self-improving evolutionary process. 

LLMs as variation operators bring two critical innovations: the ability to interpret high-level instructions, eliminating the need for step-by-step programming, and the capacity for sophisticated heuristic manipulation through natural language. When coupled with reflective optimization strategies like those in ReEvo, LLMs offer a dynamic, self-improving approach to EAs, pushing the boundaries of what traditional operators can achieve. 

# _5.3. Fitness Evaluation in Heuristic Optimization_ 

The quality of solutions for optimization problems can be evaluated directly by the objective function. In contrast, heuristics operate at a higher level of abstraction, as they represent strategies for generating solutions. Therefore, evaluating heuristics requires a mapping from the heuristic space to the solution space, followed by the application of fitness evaluation. This requires a more flexible and generalizable fitness function capable of capturing performance across diverse scenarios. To address this challenge, we summarize two primary approaches: 

- **Adaptive fitness evaluation** dynamically adjusts the criteria for assessing heuristic performance as the optimization progresses. It allows for broader exploration early in the process and more focused refinement as the search converges. AutoRNet [49] designs an **adaptive fitness function** (AFF) to dynamically adjust constraints during the evolutionary process. Initially, constraints on degree distribution are relaxed, allowing for broader exploration of the heuristic search space. As the optimization progresses, these constraints are progressively tightened, promoting convergence toward more optimal solutions while maintaining diversity within the population. This **progressive tightening** ensures that the search space is thoroughly explored while gradually refining the candidate heuristics to meet increasingly stringent requirements. 

- **Benchmark-based evaluation** ensures that heuristics generalize across multiple problem instances by testing them in a variety of scenarios, reducing the risk of overfitting to a specific instance and ensuring that the heuristic performs well in different contexts. LLaMEA [79] leverages benchmark-based fitness evaluation, utilizing platforms like IOHexperimenter to systematically assess the performance of generated metaheuristics. LLaMEA evaluates algorithms across a wide range of benchmark functions, providing a robust and reproducible environment for fitness assessment. This evaluation method promotes fairness and consistency by comparing new algorithms to well-established state-of-the-art benchmarks. 

While adaptive fitness evaluation and benchmark-based methods effectively address the generalization challenge, some problems still pose significant computational challenges, particularly when fitness evaluations are time-consuming or when heuristics generate solutions across multiple problem instances. In these cases, surrogate models provide a crucial solution. Traditional surrogate models, usually using **Gaussian Processes** and **Neural Networks** [85], have long been used in EAs. However, they come with their own set of limitations, such as the need for iterative training and updating as new data becomes available. This adds additional computational overhead, potentially diminishing their efficiency in real-time optimization tasks. 

14 

A novel method, as proposed in recent research, is the use of LLMs as surrogate models [74]. LLMs, with their powerful inference capabilities, offer a unique approach by eliminating the need for iterative training. LLMs can act as classifying solutions as “good” or “bad” based on prior performance and approximating the fitness values of new solutions based on the patterns identified in historical data. This method not only reduces the computational cost but also speeds up the optimization process, enabling the evaluation of complex problems such as network robustness without requiring full-scale evaluations for every candidate solution. 

In summary, the fitness evaluation process for heuristics presents challenges due to the need for generalization and computational efficiency. The combined use of **adaptive fitness evaluation** , **benchmark-based evaluation** , and **LLMs as surrogate models** addresses these challenges by offering flexible, scalable, and efficient methods for fitness evaluation. These approaches ensure that heuristics are not only evaluated accurately across multiple instances, but also do so with reduced computational cost. 

# **6. Future Research Directions** 

As LLM-EA automated optimization approaches continue to evolve, there are several promising areas of research that can enhance their ability. This section outlines four critical directions that could drive future advancements in the field. 

# _6.1. Enhancing Explainability and Reasoning Capabilities_ 

One of the key challenges in combining LLMs with EAs is the lack of transparency in the decision-making process of LLM-generated heuristics. The need for explainable AI (XAI) [86, 87, 88] is essential to allow researchers and practitioners to understand why specific optimization strategies are generated and how they contribute to robust solutions. Explainability not only improves trust in AI systems but also provides a foundation for diagnosing errors and refining heuristics. 

Furthermore, improving the reasoning capabilities of LLMs is crucial for developing more effective optimization heuristics. Recent advancements like Self-Taught Reasoner (STaR) [89, 90, 91] highlight the potential of iterative reasoning to refine outputs over multiple steps. STaR improves the accuracy of LLM-generated solutions by enabling the model to reason through a problem progressively rather than providing a single-shot response. Incorporating such reasoning mechanisms into LLM-EA systems can lead to more sophisticated and nuanced optimization strategies. 

# _6.2. Integration of Domain Knowledge_ 

While LLMs are trained on vast amounts of data, their general knowledge may not always be sufficient to solve domain-specific optimization problems [92]. To address this, integrating domain-specific knowledge can significantly enhance the quality and relevance of generated heuristics. Retrieval-Augmented Generation (RAG) [93, 94, 95] provides a promising approach to this challenge by combining LLMs with external knowledge sources. By retrieving relevant domain-specific information from large datasets or expert systems, LLMs can generate more specialized and effective heuristics for particular fields such as logistics, network design, or healthcare optimization. 

In addition, long memory models [96, 97] can play a crucial role in maintaining domain-specific context over extended problem-solving processes. These models enable LLMs to retain and recall relevant information from previous interactions, allowing for more coherent and context-aware heuristic generation over time. The ability to leverage both short-term and long-term knowledge will be vital in addressing complex, multi-stage optimization problems. 

# _6.3. Optimization of Evaluation and Benchmarking Platforms_ 

To ensure that LLM-generated heuristics are robust and widely applicable, there is a need for unified evaluation platforms that can consolidate training data from a wide variety of optimization problems. Such platforms would enhance the generalization capabilities of the generated heuristics by exposing them to diverse problem sets. The broad range of training data available through these platforms can help ensure that the LLM-EA systems do not overfit to a specific problem domain, thereby improving their versatility and applicability across multiple domains. 

In addition, surrogate models [74, 98, 99] can be integrated into these platforms to speed up the evaluation process. Surrogate models approximate the fitness function using historical data, which reduces the computational cost of evaluating large-scale optimization problems. This allows for faster heuristic testing and validation with limited 

15 

compromising the accuracy of results. Additionally, these platforms can include benchmarking systems that provide a standardized way to compare the performance of LLM-EA-generated heuristics against established optimization methods, fostering greater transparency and enabling further improvements through iterative development. 

# _6.4. Scalability of LLM-EA Systems_ 

As optimization problems increase in complexity and scale, ensuring the scalability of LLM-EA systems becomes a critical challenge. Distributed computing and model compression offer promising solutions to address these challenges. 

Distributed computing [100, 101] enables the parallel execution of tasks by distributing the computational load across multiple machines. This approach is particularly beneficial in the context of EAs, where large populations of candidate solutions need to be evaluated simultaneously. By leveraging distributed computing, different stages of the evolutionary process, such as selection, mutation, and crossover, can be run concurrently, reducing the overall runtime. Similarly, LLM inference tasks, such as generating new heuristics or solutions, can be distributed across multiple nodes, accelerating the optimization process. Distributed systems, therefore, provide the necessary scalability for applying LLM-EA systems to large-scale optimization problems. 

Model compression [102, 103] techniques further enhance scalability by reducing the size and computational complexity of LLMs. Methods such as pruning, quantization, and knowledge distillation allow LLMs to maintain high performance while significantly reducing their memory footprint and inference times. This is particularly valuable when LLMs are repeatedly queried during the evolutionary process. Compressed models not only run more efficiently but also reduce the energy consumption required for large-scale optimization, making LLM-EA systems more feasible for real-world applications where computational resources are limited. 

# **7. Conclusion** 

In this paper, we highlight the significant potential of the LLM-EA framework to transform the field of automated optimization, providing a new avenue for fully automated optimization. We began by tracing the evolution of heuristic approaches, establishing the need for more adaptive and automated solutions, followed by a comprehensive review of existing research on applying LLMs to optimization. By identifying the most common and valuable part of current research, we propose a novel paradigm that integrates LLMs and EAs to advance automated optimization. LLMs, with their robust generative and reasoning capabilities, play a dual role in our proposed paradigm as both heuristic designers and solution generators. By combining these strengths with the iterative search and refinement processes of EAs, the paradigm enables the automated generation of high-quality heuristics and solutions with minimal manual intervention. 

We then make a thorough analysis into the novel methodologies for individual representation, variation operators, and fitness evaluation within the LLM-EA paradigm. Our review and the proposed paradigm lay a strong foundation for future research into the capabilities of LLMs and EAs, opening up new avenues for both academic inquiry and practical applications, with the potential to reshape the landscape of optimization methodologies in a wide range of fields. 

In identifying future directions, we addressed ongoing challenges such as improving the transparency and explainability of LLM-generated heuristics, enhancing generalization to broader problem spaces, and optimizing computational efficiency. Additionally, we pointed out the integration of domain-specific knowledge and the development of scalable benchmarking platforms to further refine the efficacy and reliability of LLM-EA systems. 

# **References** 

- [1] C. A. Floudas, P. M. Pardalos (Eds.), Encyclopedia of Optimization, 2nd Edition, Springer, New York, NY, 2009. 

- [2] M. Hjeij, A. Vilks, A brief history of heuristics: how did research on heuristics evolve?, Humanities & Social Sciences Communications 10 (2023) 64. 

- [3] P. M. Pardalos, M. G. Resende (Eds.), Handbook of Metaheuristics, Springer, Boston, MA, 2003. 

- [4] R. Martí, M. Sevaux, K. Sörensen, 50 years of metaheuristics, European Journal of Operational Research (2024). 

[5] J. H. Holland, Adaptation in Natural and Artificial Systems, MIT Press, Cambridge, MA, 1975. 

- [6] S. Kirkpatrick, C. D. Gelatt, M. P. Vecchi, Optimization by simulated annealing, Science 220 (1983) 671–680. 

16 

- [7] E. K. Burke, M. R. Hyde, G. Kendall, G. Ochoa, E. Ozcan, J. R. Woodward, A comprehensive analysis of hyper-heuristics, Journal of the Operational Research Society 61 (2010) 1697–1724. 

- [8] E. K. Burke, M. Gendreau, M. Hyde, G. Kendall, G. Ochoa, R. Qu, Hyper-heuristics: a survey of the state of the art, Journal of the Operational Research Society 64 (12) (2013) 1695–1724. 

- [9] H. Naveed, A. U. Khan, S. Qiu, M. Saqib, S. Anwar, M. Usman, N. Akhtar, N. Barnes, A. Mian, A comprehensive overview of large language models, arXiv:2307.06435 (2023). 

- [10] K. A. De Jong, Evolutionary Computation: A Unified Approach, MIT Press, Cambridge, MA, 2006. 

- [11] F. Glover, G. Gutin, A. Yeo, A. Zverovich, Construction heuristics for the asymmetric TSP, European Journal of Operational Research 129 (3) (2001) 555–568. 

- [12] E. Aarts, J. K. Lenstra, Local Search in Combinatorial Optimization, Princeton University Press, 2003. 

- [13] C. Voudouris, E. Tsang, Guided local search, in: Handbook of Metaheuristics, 1999, pp. 185–218. 

- [14] A. Alsheddy, C. Voudouris, E. P. K. Tsang, A. Alhindi, Guided local search, in: R. M. et al. (Ed.), Handbook of Heuristics, 2016. [15] G. A. Croes, A method for solving traveling salesman problems, Operations Research 6 (6) (1958) 791–812. 

- [16] Y. S. Ong, M. H. Lim, X. S. Chen, Research frontier: memetic computation-past, present & future, IEEE Computational Intelligence Magazine 5 (2) (2010) 24–36. 

- [17] J. Kennedy, R. Eberhart, Particle swarm optimization, in: Proceedings of International Conference on Neural Networks, Vol. 4, 1995, pp. 1942–1948. 

- [18] M. Dorigo, V. Maniezzo, A. Colorni, Ant system: optimization by a colony of cooperating agents, IEEE Transactions on Systems, Man, and Cybernetics, Part B 26 (1) (1996) 29–41. 

- [19] Q. Zhao, Q. Duan, B. Yan, S. Cheng, Y. Shi, Automated design of metaheuristic algorithms: a survey, arXiv:2303.06532v3 (2024). 

- [20] K. Tang, X. Yao, Learn to optimize – a brief overview, National Science Review 11 (2024) nwae132. 

- [21] J. Devlin, M.-W. Chang, K. Lee, K. Toutanova, BERT: pre-training of deep bidirectional transformers for language understanding, in: Proceedings of the 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics, 2019, pp. 4171–4186. 

- [22] I. D. Mienye, T. G. Swart, G. Obaido, Recurrent neural networks: a comprehensive review of architectures, variants, and applications, MDPI Information 15 (2024). 

- [23] S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Computation 9 (8) (1997) 1735–1780. 

- [24] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, I. Polosukhin, Attention is all you need, in: Proceedings of the 31st Conference on Neural Information Processing Systems (NIPS 2017), Vol. 30, 2017. 

- [25] S. Schulhoff, M. Ilie, N. Balepur, K. Kahadze, A. Liu, C. Si, Y. Li, A. Gupta, H. Han, S. Schulhoff, P. S. Dulepet, S. Vidyadhara, D. Ki, S. Agrawal, C. Pham, G. Kroiz, F. Li, H. Tao, A. Srivastava, H. D. Costa, S. Gupta, M. L. Rogers, I. Goncearenco, G. Sarli, I. Galynker, D. Peskoff, M. Carpuat, J. White, S. Anadkat, A. Hoyle, P. Resnik, The prompt report: a systematic survey of prompting techniques, arXiv:2406.06608 (2024). 

- [26] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, Y. Iwasawa, Large language models are zero-shot reasoners, arXiv:2205.11916 (2022). 

- [27] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, et al., Language models are few-shot learners, arXiv:2005.14165 (2020). 

- [28] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, D. Zhou, Chain-of-thought prompting elicits reasoning in large language models, arXiv:2201.11903 (2022). 

- [29] J. Cheng, X. Liu, K. Zheng, P. Ke, H. Wang, Y. Dong, M. Huang, Black-box prompt optimization: aligning large language models without model training, in: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, 2024, pp. 3201–3219. 

- [30] A. Sabbatella, A. Ponti, I. Giordani, A. Candelieri, F. Archetti, Prompt optimization in large language models, MDPI Mathematics 12 (6) (2024) 929. 

- [31] Q. Guo, R. Wang, J. Guo, B. Li, K. Song, X. Tan, G. Liu, J. Bian, Y. Yang, Connecting large language models with evolutionary algorithms yields powerful prompt optimizers, in: Proceedings of the 12th International Conference on Learning Representations, 2024. 

- [32] T. Sun, Y. Shao, H. Qian, X. Huang, X. Qiu, Black-box tuning for language-model-as-a-service, in: Proceedings of the 39th International Conference on Machine Learning, 2022. 

- [33] A. Chen, D. M. Dohan, D. R. So, Evoprompting: language models for code-level neural architecture search, in: Proceedings of the 37th International Conference on Neural Information Processing Systems, Red Hook, NY, USA, 2024. 

- [34] C. Fernando, D. S. Banarse, H. Michalewski, S. Osindero, T. Rocktäschel, PromptBreeder: self-referential self-improvement via prompt evolution, in: Proceedings of the 41st International Conference on Machine Learning, 2024. 

- [35] A. AhmadiTeshnizi, W. Gao, M. Udell, OptiMUS: optimization modeling using MIP solvers and large language models, arXiv:2310.06116 (2023). 

- [36] H. Chen, G. E. Constante-Flores, C. Li, Diagnosing infeasible optimization problems using large language models, arXiv:2308.12923 (2023). 

- [37] W. Chao, J. Zhao, L. Jiao, L. Li, F. Liu, S. Yang, When large language models meet evolutionary algorithms, arXiv:2401.10510 (2024). 

- [38] R. T. Lange, Y. Tian, Y. Tang, Evolution transformer: in-context evolutionary optimization, in: Proceedings of the Genetic and Evolutionary Computation Conference Companion (GECCO’24), Melbourne, Australia, 2024. 

- [39] X. Li, K. Wu, Y. B. Li, X. Zhang, H. Wang, J. Liu, Pretrained optimization model for zero-shot black box optimization, in: Proceedings of the 38th Conference on Neural Information Processing Systems, 2024. 

- [40] X. Wu, S. hao Wu, J. Wu, L. Feng, K. C. Tan, Evolutionary computation in the era of large language model: survey and roadmap, arXiv:2401.10034 (2024). 

- [41] X. Song, Y. Tian, R. T. Lange, C. Lee, Y. Tang, Y. Chen, Leverage foundation models for black-box optimization, in: Proceedings of the 41st International Conference on Machine Learning, Vol. 235 of PMLR, Vienna, Austria, 2024. 

- [42] S. Liu, S. Yu, Z. Lin, D. Pathak, D. Ramanan, Language models as black-box optimizers for vision-language models, arXiv:2309.05950v2 (2023). 

- [43] F. Jin, Y. Liu, Y. Tan, Zero-shot chain-of-thought reasoning guided by evolutionary algorithms in large language models, 

17 

- arXiv:2402.05376v1 (2024). 

- [44] H. Yang, K. Li, InstOptima: evolutionary multi-objective instruction optimization via large language model-based instruction operators, arXiv:2310.17630v1 (2023). 

- [45] Y. B. Li, K. Wu, SPELL: semantic prompt evolution based on a LLM, arXiv:2310.01260v1 (2023). 

- [46] P.-F. Guo, Y.-H. Chen, Y.-D. Tsai, S.-D. Lin, Towards optimizing with large language model, in: Workshop on Knowledge-Infused Learning Co-located with 30th ACM KDD Conference, Barcelona, Spain, 2024. 

- [47] J. Mao, D. Zou, L. Sheng, S. Liu, C. Gao, Y. Wang, Y. Li, Identify critical nodes in complex network with large language models, arXiv:2403.03962 (2024). 

- [48] S. Mo, K. Wu, Q. Gao, X. Teng, J. Liu, AutoSGNN: automatic propagation mechanism discovery for spectral graph neural networks, Under Review (2024). 

- [49] H. Yu, J. Liu, AutoRNet: automatically optimizing heuristics for robust network design via large language models, under Review (2024). 

- [50] B. Huang, X. Wu, Y. Zhou, J. Wu, L. Feng, R. Cheng, K. C. Tan, Exploring the true potential: evaluating the black-box optimization capability of large language models, arXiv:2404.06290 (2024). 

- [51] H. Ghaemi, Z. Alizadehsani, A. Shahraki, J. M. Corchado, Transformers in source code generation: a comprehensive survey, Journal of Systems Architecture 153 (2024) 103193. 

- [52] H. Luo, J. Wu, J. Liu, M. F. Antwi-Afari, Large language model-based code generation for the control of construction assembly robots: a hierarchical generation approach, Developments in the Built Environment 19 (2024) 100488. 

- [53] E. Meyerson, M. J. Nelson, H. Bradley, A. Gaier, A. Moradi, A. K. Hoover, J. Lehman, Language model crossover: variation through few-shot prompting, arXiv:2302.12170 (2024). 

- [54] J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh, K. O. Stanley, Evolution through large models, in: Handbook of Evolutionary Machine Learning, Springer, 2023, pp. 331–366. 

- [55] E. Hemberg, S. Moskal, U.-M. O’Reilly, Evolving code with a large language model, arXiv:2401.07102 (2024). 

- [56] C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, X. Chen, Large language models as optimizers, in: Proceedings of the International Conference on Learning Representations (ICLR), 2024. 

- [57] S. Liu, C. Chen, X. Qu, K. Tang, Y.-S. Ong, Large language models as evolutionary optimizers, arXiv:2310.19046v3 (2024). 

- [58] F. Liu, X. Lin, Z. Wang, S. Yao, X. Tong, M. Yuan, Q. Zhang, Large language model for multi-objective evolutionary optimization, arXiv:2310.12541v1 (2023). 

- [59] Z. Wang, S. Liu, J. Chen, K. C. Tan, Large language model-aided evolutionary search for constrained multiobjective optimization, arXiv:2405.05767 (2024). 

- [60] R. T. Lange, Y. Tian, Y. Tang, Large language models as evolution strategies, in: Proceedings of the Genetic and Evolutionary Computation Conference Companion (GECCO’24), Melbourne, Australia, 2024. 

- [61] S. Brahmachary, S. M. Joshi, A. Panda, K. Koneripalli, A. K. Sagotra, H. Patel, A. Sharma, A. D. Jagtap, K. Kalyanaraman, Large language model-based evolutionary optimizer: reasoning with elitism, arXiv:2403.02054 (2024). 

- [62] M. Pluhacek, A. Kazikova, T. Kadavy, A. Viktorin, R. Senkerik, Leveraging large language models for the generation of novel metaheuristic optimization algorithms, in: Proceedings of the Genetic and Evolutionary Computation Conference Companion (GECCO), Lisbon, Portugal, 2023. 

- [63] M. Pluhacek, J. Kovac, A. Viktorin, P. Janku, T. Kadavy, R. Senkerik, Using LLM for automatic evolvement of metaheuristics from swarm algorithm SOMA, in: Proceedings of the Genetic and Evolutionary Computation Conference Companion (GECCO’24), Melbourne, Australia, 2024. 

- [64] R. Zhong, Y. Xu, C. Zhang, J. Yu, Leveraging large language model to generate a novel metaheuristic algorithm with CRISPE framework, Cluster Computing (2024). 

- [65] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. R. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, P. Kohli, A. Fawzi, Mathematical discoveries from program search with large language models, Nature 625 (2024) 468–475. 

- [66] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, Q. Zhang, Evolution of heuristics: towards efficient automatic algorithm design using large language model, in: Proceedings of International Conference on Machine Learning (ICML), 2024. 

- [67] F. Liu, X. Tong, M. Yuan, Q. Zhang, Algorithm evolution using large language model, arXiv:2311.15249v1 (2023). 

- [68] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, Q. Zhang, An example of evolutionary computation + large language model beating human: design of efficient guided local search, arXiv:2401.02051v1 (2024). 

- [69] F. Arnold, K. Sörensen, Knowledge-guided local search for the vehicle routing problem, Computers and Operations Research 105 (2019) 32–46. 

- [70] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim, J. Park, G. Song, Large language models as hyper-heuristics for combinatorial optimization, arXiv:2402.01145v2 (2024). 

- [71] Y. Sun, X. Zhang, S. Huang, S. Cai, B. Zhang, K. Wei, AutoSAT: automatically optimize sat solvers via large language models, arXiv:2402.10705 (2024). 

- [72] Y. Huang, S. Wu, W. Zhang, J. Wu, L. Feng, K. C. Tan, Autonomous multi-objective optimization using large language model, arXiv:2406.08987 (2024). 

- [73] Y. Huang, X. Lv, S. Wu, J. Wu, L. Feng, K. C. Tan, Advancing automated knowledge transfer in evolutionary multitasking via large language models, arXiv:2409.04270 (2024). 

- [74] H. Hao, X. Zhang, A. Zhou, Large language models as surrogate models in evolutionary algorithms: a preliminary study, Swarm and Evolutionary Computation 91 (2024) 101741. 

- [75] O. Kramer, Large language models for tuning evolution strategies, arXiv:2405.10999 (2024). 

- [76] L. L. Custode, F. Caraffini, A. Yaman, G. Iacca, An investigation on the use of large language models for hyperparameter tuning in evolutionary algorithms, in: Proceedings of the Genetic and Evolutionary Computation Conference Companion (GECCO’24), Melbourne, VIC, Australia, 2024. 

- [77] M. Zhou, J. Liu, A two-phase multi-objective evolutionary algorithm for enhancing the robustness of scale-free networks against multiple 

18 

malicious attacks, IEEE Transactions on Cybernetics 47 (2) (2017) 539–552. 

- [78] M. Zhou, J. Liu, A memetic algorithm for enhancing the robustness of scale-free networks against malicious attacks, Physica A: Statistical Mechanics and its Applications 410 (2014) 131–143. 

- [79] N. van Stein, T. Bäck, LLaMEA: a large language model evolutionary algorithm for automatically generating metaheuristics, arXiv:2405.20132 (2024). 

- [80] W. E. Hart, N. Krasnogor, Using multiple representations in evolutionary algorithms, in: Proceedings of the Genetic and Evolutionary Computation Conference, 1998, pp. 359–366. 

- [81] K. Deb, Representation, selection, and variation in genetic algorithms, Genetic Algorithms in Engineering and Computer Science (1997) 78–98. 

- [82] W. M. Spears, Crossover or mutation?, Foundations of Genetic Algorithms 2 (1995) 221–237. 

- [83] T. Jones, S. Forrest, Fitness distance correlation as a measure of problem difficulty for genetic algorithms, in: Proceedings of the 6th International Conference on Genetic Algorithms, 1995, pp. 184–192. 

- [84] M. Mitchell, S. Forrest, J. H. Holland, The royal road for genetic algorithms: fitness landscapes and GA performance, in: Proceedings of the 1st European Conference on Artificial Life, 1992, pp. 245–254. 

- [85] J. A. Garcia, H. Zhenli, Gaussian process regression + deep neural network autoencoder for probabilistic surrogate modeling in nonlinear mechanics of solids, arXiv:2407.10732 (2024). 

- [86] M. T. Ribeiro, S. Singh, C. Guestrin, Why should I trust you? Explaining the predictions of any classifier, in: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016, pp. 1135–1144. 

- [87] M. T. Ribeiro, S. Singh, C. Guestrin, Lime: local interpretable model-agnostic explanations, in: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016, pp. 1135–1144. 

- [88] W. Samek, T. Wiegand, K.-R. Müller, Explainable artificial intelligence: understanding, visualizing and interpreting deep learning models, arXiv:1708.08296 (2017). 

- [89] E. Zelikman, Y. Wu, J. Mu, N. D. Goodman, STaR: bootstrapping reasoning with reasoning, arXiv:2203.14465 (2022). 

- [90] A. Hosseini, X. Yuan, N. Malkin, A. Courville, A. Sordoni, R. Agarwal, V-STaR: training verifiers for self-taught reasoners, arXiv:2403.09629 (2024). 

- [91] E. Zelikman, G. Harik, Y. Shao, V. Jayasiri, N. Haber, N. D. Goodman, Quiet-STaR: language models can teach themselves to think before speaking, arXiv:2403.09629 (2024). 

- [92] R. Zhang, F. Liu, X. Lin, Z. Wang, Z. Lu, Q. Zhang, Understanding the importance of evolutionary search in automated heuristic design with large language models, arXiv:2407.10873v1 (2024). 

- [93] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. tau Yih, T. Rocktäschel, S. Riedel, D. Kiela, Retrieval-augmented generation for knowledge-intensive NLP tasks, in: Proceedings of the 33th International Conference on Neural Information Processing Systems, 2020, pp. 9459–9474. 

- [94] K. Guu, K. Lee, Z. Tung, P. Pasupat, M.-W. Chang, REALM: retrieval-augmented language model pre-training, in: Proceedings of the 37th International Conference on Machine Learning, 2020, pp. 3929–3938. 

- [95] G. Izacard, E. Grave, Fusion-in-Decoder: a novel retrieval-augmented language model, in: Proceedings of the 2021 Annual Conference of the North American Chapter of the Association for Computational Linguistics, 2021, pp. 681–688. 

- [96] M. Burtsev, A. V. Kurenkov, Memorizing transformers, arXiv:2010.06891 (2020). 

- [97] J. W. Rae, A. Potapenko, S. M. Jayakumar, T. P. Lillicrap, Compressive transformers for long-range sequence modeling, in: Proceedings of the 32th International Conference on Neural Information Processing Systems, 2019, pp. 4694–4707. 

- [98] L. Bliek, A. Guijt, R. Karlsson, S. Verwer, M. de Weerdt, Benchmarking surrogate-based optimisation algorithms on expensive black-box functions, Applied Soft Computing 147 (2023) 110744. 

- [99] T. Rios, F. Lanfermann, S. Menzel, Large language model-assisted surrogate modelling for engineering optimization, in: Proceedings of 2024 IEEE Conference on Artificial Intelligence (CAI), 2024, pp. 796–803. 

- [100] J. Dean, S. Ghemawat, MapReduce: simplified data processing on large clusters, Communications of the ACM 51 (1) (2008) 107–113. 

- [101] Y. Tang, Y. Tian, R. Huang, Distributed learning with evolutionary algorithms, in: Proceedings of the Genetic and Evolutionary Computation Conference (GECCO), 2021, pp. 851–859. 

- [102] S. Han, J. Pool, J. Tran, W. Dally, Deep compression: compressing deep neural networks with pruning, trained quantization and huffman coding, arXiv:1510.00149 (2015). 

- [103] G. Hinton, O. Vinyals, J. Dean, Distilling the knowledge in a neural network, in: Proceedings of the NIPS Deep Learning and Representation Learning Workshop, 2015. 

19 

