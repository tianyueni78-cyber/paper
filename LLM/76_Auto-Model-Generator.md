# **Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer** 

## Boris Almonacid 

boris.almonacid@globalchange.science 

Global Change Science 

Puerto Varas, Chile 

### **ABSTRACT** 

This article presents a framework for generating optimisation models using a pre-trained generative transformer. The framework involves specifying the features that the optimisation model should have and using a language model to generate an initial version of the model. The model is then tested and validated, and if it contains build errors, an automatic edition process is triggered. An experiment was performed using MiniZinc as the target language and two GPT-3.5 language models for generation and debugging. The results show that the use of language models for the generation of optimisation models is feasible, with some models satisfying the requested specifications, while others require further refinement. The study provides promising evidence for the use of language models in the modelling of optimisation problems and suggests avenues for future research. 

### **CCS CONCEPTS** 

• **Mathematics of computing** → **Combinatoric problems** ; • **Theory of computation** → **Discrete optimisation** ; • **Computer systems organization** → **High-level language architectures** ; • **Software and its engineering** → **Source code generation** ; • **Computing methodologies** → **Natural language processing** . 

### **KEYWORDS** 

Automatic Optimisation Models, MiniZinc, Large Language Models, Generative Pre-trained Transformer, GPT-3.5 

### **1 INTRODUCTION** 

Optimisation models play a critical role in many industries, including healthcare, energy, food industry, and transportation. However, creating an accurate and efficient model can be a timeconsuming task as you have to learn modelling languages. To address this challenge, this paper proposes an automatic optimisation model generator that is assisted by a pre-trained generative transformer (GPT) [5]. Recent advances in natural language processing [2] have led to the development of powerful large language models, such as GPT-3, that can generate high-quality text. The use of GPT for software error correction has been demonstrated in prior work [4], which provides a basis for its potential application in other 

domains, including optimisation problem modelling. Taking advantage of the capabilities of these models and progress, this research aims to automate the optimisation model generation process by initially defining the necessary features of the problem and using the language model to generate an initial version of the model or repair it in case of finding errors. This approach has the potential to significantly improve the speed and accuracy of optimisation model generation, making it possible to quickly generate models that meet desired specifications. Additionally, it can help reduce the expertise required to build these models, making the process accessible to a broader audience. 

### **2 THE METHOD** 

The approach is outlined in Figure 1. The user specifies the desired features of the optimisation model through a prompt. These instructions are the input of the GPT Agent, which is responsible for generating the optimisation model. Once the model is created, it is sent to the optimisation agent, which has the function of compiling and executing the optimisation model. In the event that the optimisation agent compiles the model and solves it satisfactorily, the optimisation model and the solution are provided to the user as a result. The event in which the optimisation model contains compilation errors triggers an automatic fixed process, whereby the error message is used to provide feedback and resolve problems in the model. Algorithm 1 describes the steps mentioned above. 



<!-- Start of picture text -->
input write get Model output<br>Prompt and<br>Solution<br>User<br>Pre-trained Generative<br>Optimisation Agent<br>Transformer Agent<br>create<br>Optimisation Model model<br>Generation Solver<br>Auto Fixed update<br>model<br>Model<br>error<br>feedback<br><!-- End of picture text -->

**Figure 1: Outline of the Automatic Optimisation Model Generator Assisted with a Pre-trained Generative Transformer.** 

Boris Almonacid ORCID: https://orcid.org/0000-0002-6367-9802 Preprint log: 

> - 14 Apr 2023: Submitted to Genetic and Evolutionary Computation Conference (GECCO-2023) as Late-Breaking Abstract. 

> - 03 May 2023: Reject by GECCO-2023. 

> - 09 May 2023: Submitted to arXiv. 

Boris Almonacid 

**Algorithm 1: Automatic Optimisation Model Generator** 

1 <mark>instruction = "Me: A source code with 10 discrete</mark> 2 <mark>variables."</mark> 3 <mark>model = optimisation_model_generator (instruction)</mark> 4 <mark>while True :</mark> 5 <mark>status , output = solver (model)</mark> 6 <mark>if status == True :</mark> 7 <mark>return output</mark> 8 <mark>else:</mark> 9 <mark>input = model</mark> 10 <mark>instruction = "Me: Fix the minizinc code. The Error</mark> 11 <mark>code is " + output + "Bot:"</mark> 12 <mark>model = auto_fixed_model (input , instruction)</mark> 

### **3 EXPERIMENT** 

The MiniZinc<sup>1</sup> modelling language [3] has been used as the target language for the generation of optimisation models. The models were solved by Gecode 6.3.0. The experimentation protocol involves the utilisation of two distinct GPT-3.5 language models<sup>2</sup> for the generation of the tests. For the generation of an initial optimisation model, the text-davinci-003 model will be used, it is a large language model that uses a combination of neural network techniques to generate coherent and well-structured text. On the other hand, the text-davinci-edit-001 model<sup>3</sup> will be used that focuses on text editing and error correction. The parameters used in the functions for code generation and automatic code editing are described in the Algorithm 2. 

#### **Algorithm 2: Parameters of GPT functions** 



<!-- Start of picture text -->
1 def optimisation_model_generator (instruction: str ):<br>2 response = openai.Completion.create(model="text -<br>davinci -003" , prompt=instruction , temperature =0,<br>max_tokens =200, top_p=1, frequency_penalty =0.0,<br>presence_penalty =0.0, stop=[ "Bot:" , "Me:" ])<br>3 return response.choices [0].text , response<br>4<br>5 def auto_fixed_model (input: str , instruction: str ):<br>6 response = openai.Edit.create(model="text -davinci -<br>edit -001" , input=input , instruction=instruction ,<br>temperature =0, top_p =1)<br>7 return response.choices [0].text , response<br><!-- End of picture text -->

The test involves 10 instances, with the first 5 involving discrete variables and the last 5 involving a matrix composed of discrete variables. For each instance, the test considers whether the domain of the variable is open or defined, and whether or not a constraint applies. These instances will be entered into the system through a prompt<sup>4</sup> indicating these features. The MiniZinc Python library<sup>5</sup> is used for run-time validation of the optimisation model. In order to ensure whether the obtained optimisation model is correct according to the instructions in the prompt, a manual inspection of the generated source code is performed. 

> 1 The version used was MiniZinc 2.7.1, https://www.minizinc.org 

> 2 https://platform.openai.com/docs/models/gpt-3-5 

> 3 https://openai.com/blog/gpt-3-edit-insert 

> 4 “Bot: Ask me any questions about the MiniZinc. MiniZinc is a high-level constraint programming language used for modelling and solving combinatorial optimisation problems. Me: Can I ask you about codes written in MiniZinc as an example? Can you show only the source code? Bot: Yes. Tell me what kind of language optimisation problems MiniZinc would like me to generate for you. Me: A source code with 10 discrete variables without domain and without constraints. Put the Bot comments with % symbol. Bot:” 

> 5 https://github.com/MiniZinc/minizinc-python 

**Table 1: Results of the tests in the automatic generation of MiniZinc models.** 

|ID|Variable|Domain|Const.|Valid|Correct|Step|Token|
|---|---|---|---|---|---|---|---|
|1|discrete|open|no|yes|yes|2|508|
|2|discrete|open|yes|yes|yes|2|584|
|3|discrete|defined|no|yes|yes|1|170|
|4|discrete|defined|yes|yes|yes|1|205|
|5|discrete|defined|all_diff|no|no|10|1712|
|6|array disc.|open|no|yes|no|2|293|
|7|array disc.|open|yes|yes|no|2|359|
|8|array disc.|defined|no|yes|no|2|337|
|9|array disc.|defined|yes|yes|yes|2|349|
|10|array disc.|defined|all_diff|no|no|10|1787|



> a The valid column indicates that the model is valid in its execution. The correct column indicates that the generated model corresponds to what was requested. 

> b The data supporting this study’s results are available in Figshare at [1]. 

The results of the tests are described in Table 1. The results indicate that the use of GPT-3.5 language models for the generation of optimisation models in MiniZinc is feasible. The models generated for instances 1, 2, 3, 4, and 9 were valid and met the requested specifications. However, the models generated for instances 5 and 10 despite including the all_different constraint, the include "alldifferent.mzn"; library was omitted from both models. Models have been generated for instances 6, 7 and 8 that are valid. However, the models do not meet the requested specifications. 

### **4 CONCLUSIONS** 

In conclusion, this study provides promising evidence for the use of GPT-3.5 language models in the automatic modelling of optimisation problems. Future research could explore other language models and evaluate their performance compared to the GPT-3.5 models used in this study. Additionally, future studies could explore the use of other optimisation problem modelling languages, in the study of more explicit error messages and user-centered and machine-centered error messages. 

### **ACKNOWLEDGMENTS** 

Boris Almonacid acknowledges the support of PhD (h.c) Sonia Alvarez, Chile. The founders had no role in study design, data collection and analysis, the decision to publish, or the preparation of the manuscript. This study was not externally funded, including by the Chilean Government or any Chilean Universities. 

### **REFERENCES** 

> [1] Boris Almonacid. 2023. Dataset for Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer. https://doi.org/10. 6084/m9.figshare.22582387 

> [2] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ (2021). 

> [3] Nicholas Nethercote, Peter J Stuckey, Ralph Becket, Sebastian Brand, Gregory J Duck, and Guido Tack. 2007. MiniZinc: Towards a standard CP modelling language. In _Principles and Practice of Constraint Programming–CP 2007: 13th International Conference, CP 2007, Providence, RI, USA, September 23-27, 2007. Proceedings 13_ . Springer, 529–543. 

Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer 

- [4] Dominik Sobania, Martin Briesch, Carol Hanna, and Justyna Petke. 2023. An analysis of the automatic bug fixing performance of chatgpt. _arXiv preprint arXiv:2301.08653_ (2023). 

- [5] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. _Advances in neural information processing systems_ 30 (2017). 

