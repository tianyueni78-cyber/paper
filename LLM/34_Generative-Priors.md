# **Sample-Efficient Optimization over Generative Priors via Coarse Learnability** 

**Pranjal Awasthi Sreenivas Gollapudi Ravi Kumar** _Google Research, Mountain View, USA †_ **Kamesh Munagala** 

PRANJALAWASTHI@GOOGLE.COM SGOLLAPU@GOOGLE.COM RAVI.K53@GMAIL.COM 

KAMESH@CS.DUKE.EDU 

_Department of Computer Science, Duke University, Durham, USA_ 

## **Abstract** 

We study zeroth-order optimization where solutions must minimize a cost _d_ ( _s_ ) while maintaining high probability under a complex generative prior _L_ ( _s_ ) (e.g., a parameterized model). This reduces to sampling from a target distribution proportional to _L_ ( _s_ ) _e_<sup>_−T ·d_(</sup><sup>_s_)</sup> . Since classical model-based optimization (MBO) lacks finite-sample guarantees for expressive approximate learners, we introduce _coarse learnability_ , a flexible statistical assumption requiring only that a learned model covers the target’s probability mass within a polynomial factor. 

Leveraging this assumption, we design an iterative MBO algorithm called ALDRIFT with a sample correction step that provably approximates the target using only a polynomial number of samples. We apply this framework to globally optimizing non-convex objectives bounded by a quadratic envelope in R<sup>_n_</sup> , where we show this assumption is naturally satisfied for a family of “optimistic” posterior distributions. To reach global _ε_ -optimality, this implies a sample complexity of _O_<sup>�</sup> (log 1 _/ε_ ), a rate characteristic of optimistic space-partitioning methods. 

We further justify coarse learnability as an assumption for generative priors theoretically, proving that in simple settings, parametric maximum likelihood estimation and over-smoothed kernel density estimators naturally satisfy it. 

Finally, one motivation for our framework comes from inference-time alignment. Though our primary contribution pertains to the theoretical foundations of MBO, we provide qualitative evidence that, in simple settings, even primitive LLMs can shift their distributions toward lowercost regions when fine-tuned with zeroth-order feedback. 

## **1. Introduction** 

Model-based optimization (MBO) is a broadly applicable framework for zeroth-order optimization: a probabilistic model over candidate solutions is iteratively updated using function evaluations, guiding search toward high-performing solutions. Classical MBO methods such as the crossentropy method (Rubinstein, 1999) are well-studied and widely used, but their theoretical guarantees are asymptotic (as opposed to finite sample) and rely on strong structural assumptions. These assumptions break down when the generative model is an expressive approximate learner, such as a neural network, leaving the finite-sample behavior of MBO in this regime theoretically uncharacterized. As discussed more in Section 8, a motivating instance is inference-time optimization with learned generative priors, including language models, where one seeks to enforce global objectives while retaining high prior likelihood under the generative model. While analyzing MBO over modern generative models remains challenging, establishing finite-sample guarantees in tractable, continuous domains is a necessary first step. This requires more flexible assumptions on the generative model, which is the focus of this paper. 

> _†_ This work was done while the author was visiting Google Research. 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

### **1.1. Model-Based Optimization (MBO) with a Generative Prior** 

We study a zeroth-order optimization framework, where the goal is to minimize a function _d_ ( _·_ ) given only oracle access to its values. The function _d_ ( _·_ ) might represent a continuous non-convex loss surface, or a discrete penalty for violating global constraints. To guide this search, we assume access to a generative prior _L_ ( _·_ ) and our objective is to sample effectively from a target distribution of the form _pT_ ( _s_ ) _∝L_ ( _s_ ) _· e_<sup>_−T·d_(</sup><sup>_s_)</sup> , where _T_ is a ‘temperature’ parameter. Samples from this distribution naturally balance low values of _d_ ( _s_ ) with high probability under the prior _L_ ( _s_ ). This formulation is versatile: in continuous domains, the prior provides regularization to escape local minima (see Section 5); in combinatorial settings, it allows a division of labor where an external checker enforces global feasibility via _d_ ( _·_ ) while a generative model enforces semantic priors via _L_ ( _·_ ). 

Our primary object in this paper is sampling from _pT_ ; approximate optimization of _d_ follows by choosing _T_ appropriately large. For such _T_ , the target distribution _pT_ can become _exponentially far_ from the initial prior _L_ , making direct sampling or simple rejection-based corrections infeasible. 

**Sample-Efficient Model-Based Optimization.** To address this sampling challenge, we adopt the perspective of model-based optimization (MBO), most notably the cross-entropy method (Rubinstein, 1999) and model reference adaptive search (Hu et al., 2007). (Section 1.2 and Appendix A.3 contain a detailed comparison.) These methods, which are widely used for derivative-free nonconvex optimization (Shahriari et al., 2016; Snoek et al., 2012), optimize an objective by iteratively updating a probabilistic or neural search distribution that concentrates on the optimum. However, classical guarantees for these methods typically rely on asymptotic convergence arguments via structural properties of specific surrogates, such as natural exponential families (Hu et al., 2007). These results do not extend to the finite-sample regime, either with well-structured priors or with generative models that function as approximate learners. Our work bridges this gap by providing polynomial sample complexity bounds for this class of algorithms under a general _coarse learnability_ assumption, replacing rigid structural constraints with a statistical coverage condition. 

**Simulated Annealing and ALDRIFT.** We operationalize this framework via ALDRIFT ( _Algorithm Driven Iterated Fitting of Targets_ ), an iterative algorithm in which a generative model is progressively refined. We construct an intermediate distribution _pτ_ ( _s_ ) _∝L_ ( _s_ ) _· e_<sup>_−τ·d_(</sup><sup>_s_)</sup> and detail how ALDRIFT treats _τ_ as a (inverse) temperature parameter—drawing inspiration from simulated annealing (Kirkpatrick et al., 1983; Kalai and Vempala, 2006; Jerrum and Sinclair, 1996)—and gradually increases it to _T_ to assign more weight to the objective _d_ (see Section 3). Crucially, at each iteration, ALDRIFT performs a Metropolis–Hastings step to generate samples from the current target distribution _pτ_ ( _s_ ), using the learned generative model as a proposal. Because we only know the target up to an unnormalized weight, estimating its normalizer or using importance (Thomas and Brunskill, 2016) or rejection sampling (Huang et al., 2025) would require exponentially many samples (see Appendix A.2). Metropolis–Hastings circumvents this by relying solely on _relative_ likelihood ratios, allowing the procedure to remain efficient even when the target and initial distributions differ exponentially. 

The resulting samples are then used to fit the new generative model (via say parameter estimation) so that it produces samples that are more closely aligned with _pτ_ ( _s_ ). At a high level, this approach is analogous to related methods in convex optimization (Kalai and Vempala, 2006), to approximate policy-iteration schemes from reinforcement learning (Schulman et al., 2015; Agar- 

2 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

wal et al., 2020; Kakade and Langford, 2002; Peters and Schaal, 2007; Peters et al., 2010), and to sequential MCMC Del Moral et al. (2006); Cappé et al. (2004); Neal (1998); Andrieu et al. (2010), though the details and objectives differ. Further, as discussed in Appendix A.3, ALDRIFT is an instance of the model reference adaptive search (MRAS) framework (Hu et al., 2007), and our algorithm and analysis can be interpreted as a finite-sample robustification of MRAS via the Metropolis–Hastings proposal step. 

**Formal Guarantees via Coarse Learnability.** Our main theoretical contribution in Section 4 is a proof that ALDRIFT converges to the target distribution _pT_ ( _s_ ) with polynomial sample complexity, under a novel coverage assumption we call _coarse learnability_ . (See Assumption 2 in Section 4 for a formal statement.) This assumption formalizes approximate learning as follows: given _m_ samples from a target distribution, we can learn a generative model whose density envelopes the target density within a factor of poly( _m_ ), except on an exponentially small error set. 

A central conceptual contribution of our work is the formulation of coarse learnability itself. At a conceptual level, as discussed in Section 4, coarse learnability identifies a sufficient statistical condition under which any sampling-based learner can provably refine a generative model toward a target distribution. As we discuss in Section 1.2, coarse learnability is related to the notion of _coverage_ in reinforcement learning (Szepesvári and Munos, 2005; Xie et al., 2023), which similarly quantifies when a policy explores enough of the optimal state-action space to permit efficient improvement. Coarse learnability differs by treating coverage as a dynamic statistical outcome of the model fitting instead of as a static assumption, regenerating the required coverage dynamically at each iteration. 

**Provable Bounds for Non-Convex Global Optimization.** Section 4 gives a general finite-sample guarantee for ALDRIFT under Assumption 2. In Section 5, we show the utility of this result in the classical setting of _ε_ -approximately globally optimizing a non-convex function in R<sup>_n_</sup> , where prior results only show asymptotic convergence of MBO with infinitely many samples Hu et al. (2007). In contrast, we prove that on a well-studied class of quadratically bounded non-convex functions (Bubeck et al., 2011; Munos, 2011) with known curvature bounds, ALDRIFT is sampleefficient. Unlike existing MBO methods that fit an exact exponential family model, we fit a wider Gaussian posterior, analogous to optimistic exploration in bandit literature (Bubeck et al., 2011). This key difference enables us to verify Assumption 2 in this setting, and show that a strengthening of ALDRIFT achieves sample complexity _O_<sup>�</sup> (log 1 _/ε_ ), with dimension- and geometry-dependent constants. This rate is characteristic of optimistic space partitioning methods (Munos, 2011; Bubeck et al., 2011) (see Section 5 for some caveats) and is exponentially better than that achievable by local MCMC methods (Holley and Stroock, 1987; Hajek, 1988). We note that for this sample-complexity guarantee, Assumption 2 is no longer an assumption, as it is rigorously verified. Complementing our theory, we present an empirical demonstration of the need for the inflated proposal and sample correction steps with limited sample budgets in Section 6. 

**Theoretical Plausibility of Coarse Learnability.** In Section 7, we present theoretical evidence justifying Assumption 2 for certain generative models. We demonstrate that standard MLE naturally induces the required coverage properties in several simplified settings: the _agnostic_ setting where the model is misspecified (e.g., a unimodal learner approximating a multimodal target) and precise density approximation is impossible; for the _realizable_ setting for well-behaved exponential families; and _non-parametric settings_ such as standard Kernel Density Estimation. 

3 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

**Motivating Application: Inference-time Alignment.** Though our primary focus is to theoretically formalize the mechanics of MBO under generative priors, we note in Section 8 that one motivating application is the combination (via inference-time alignment and fine-tuning) of classical combinatorial algorithms with generative models (Huang et al., 2025; Chen et al., 2025; Madaan et al., 2023) to solve problems that require both global feasibility and adherence to local priors: route planning with qualitative scenic preferences as prior, molecular design with learned drug-likeness priors, or scheduling with semantic session coherence. In such problems, the generative model encodes local constraints that a classical algorithm cannot capture, while the algorithm enforces global structure that a generative model cannot reliably guarantee. LLMs are a natural family of priors for this purpose, though, as we illustrate in Section 8, they can fail to enforce global combinatorial properties on their own, confirming the need for the hybrid approach. 

We present qualitative results in Section 9 demonstrating that even a relatively primitive LLM can iteratively acquire combinatorial constraints (initially unknown to it) from only a few samples via fine-tuning. Specifically, we show that for a simple scheduling problem and for low degree spanning trees, when guided by a heuristic version of ALDRIFT called TOPIFT, an LLM (GPT2 (Radford et al., 2018)) can adapt its generative distribution to favor solutions with low _d_ ( _s_ ) values while still respecting its prior, hence qualitatively demonstrating the “mass covering” type behavior required for coarse learnability. 

While our formal guarantees do not yet apply to inference-time alignment directly (and likely require relaxed formulations), our aim is to introduce an MBO framework that makes the behavior of expressive and potentially mis-specified models more amenable to analysis. By identifying coverage as a key driver of convergence, we provide a possible theoretical lens for reasoning about how generative models could support combinatorial optimization under appropriate coverage conditions. 

**Summary of Contributions.** We summarize our primary contributions as follows: 

- **Conceptual Framework:** We introduce _coarse learnability_ (Assumption 2) as a sufficient coverage-style condition to establish finite-sample guarantees for iterative Model-Based Optimization (MBO) using expressive approximate learners. 

- **MBO Algorithm:** We propose ALDRIFT (Section 3.2), an MBO algorithm that pairs iterative learning of generative models with a principled sampling correction step (e.g., MetropolisHastings) to control the accumulation of approximation errors. 

- **General Theoretical Guarantee:** We prove that under Assumption 2, ALDRIFT achieves polynomial finite-sample convergence to the target _pT_ (Theorem 1). 

- **Unconditional Instantiation:** To ground our framework, we analyze ALDRIFT in the canonical setting of _ε_ -globally optimizing non-convex objectives bounded by a quadratic envelope in R<sup>_d_</sup> in Section 5. By employing an optimistic Gaussian proposal, we show that coarse learnability holds in this setting and obtain a sample complexity of _O_<sup>�</sup> (log 1 _/ε_ ). 

- **Supporting Evidence:** Finally, we provide proof-of-concept theoretical and qualitative empirical evidence (Sections 7 and 9) demonstrating respectively that certain simple generative models satisfy coarse learnability and that even primitive LLMs can exhibit the mass-covering behavior required by our theoretical framework on combinatorial tasks. 

4 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

### **1.2. Related Work** 

Our work sits at the intersection of several active research areas, including zeroth-order optimization, statistical learning theory, sequential MCMC, and non-convex optimization. We present the most pertinent related work here, and defer related work on non-convex optimization methods to Section 5.4. 

**Model-Based Optimization and MRAS.** Our approach is formally an instance of the model reference adaptive search (MRAS) framework (Hu et al., 2007), which generalizes the cross-entropy method (Rubinstein, 1999). MRAS operates by using a parametric model to approximate a sequence of ideal target distributions that increasingly concentrate on the optimum. In each epoch, it generates samples from the current parametric model, selects the high-performing “elite” samples, and updates the model parameters to fit this elite set. While MRAS is proven to converge in the limit to the globally optimal solution when the parametric distributions are from an exponential family, it lacks sample complexity bounds, both for simple parametric families as well as for expressive approximate learners, which is the focus of our paper. We present this connection in more detail in Appendix A.3. 

Our work also bears similarity to reinforcement learning algorithms like reward-weighted regression (Peters and Schaal, 2007) and relative entropy policy search (Peters et al., 2010). These methods typically view the optimization as an Expectation-Maximization (EM) problem. Our framework differs by explicitly acknowledging that the ‘M-step’ (learning the generative model) may be imperfect (coarse). Our main contribution is modeling this coarseness and developing polynomial sample complexity bounds by correcting for these imperfections via Metropolis–Hastings. 

**Sequential Monte-Carlo Sampling.** The annealing structure of ALDRIFT, progressing through a sequence of tempered distributions _pτ_ ( _s_ ) _∝L_ ( _s_ ) _e_<sup>_−τd_(</sup><sup>_s_)</sup> with Metropolis–Hastings corrections at each step, shares a foundational skeleton with Annealed Importance Sampling (AIS; (Neal, 1998)) and Sequential Monte Carlo (SMC; (Del Moral et al., 2006; Andrieu et al., 2010)). However, these methods maintain a discrete empirical measure over particles, while ALDRIFT introduces a parametric projection step: it fits a generative model to the particles at each temperature, which is then used as the proposal for the next step. In effect, this replaces the variance associated with importance weights and particle degeneracy with approximation bias, as the fitted model _Lτ_ may not faithfully cover the target _pτ_ . While related ideas appear in adaptive and amortized sampling methods, this projection step introduces a distinct source of error not present in classical particle-based schemes, which we address via the coarse learnability assumption. 

Population Monte Carlo (PMC; Cappé et al. (2004)) shares a similar overall structure to ALDRIFT. It iteratively fits a parametric proposal to a particle population; however, it is an Importance Sampling algorithm and in our setting, the target distribution exponentially concentrates, so that the variance in weights explodes. ALDRIFT circumvents this by defining a sequence of intermediate targets and utilizing Metropolis-Hastings to draw unweighted samples from them. (See Appendix A.2 for the necessity of the M-H step). Consequently, our contribution is to present sufficient conditions under which such unweighted sampling has polynomial complexity. 

Furthermore, while recent work on amortized MCMC via transport maps similarly focuses on “learning to propose” to improve acceptance rates (Parno and Marzouk, 2018; Brofos et al., 2022; Hoffman et al., 2019), we introduce a finite-sample coverage assumption (Assumption 2) rather than relying on accuracy of the learned transport map to improve sampling efficiency. 

5 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

**Bandit Convex Optimization.** Our problem involves optimizing an objective _d_ ( _s_ ) where only function evaluations are available. This is related to bandit convex optimization (BCO) (Flaxman et al., 2005), which provides regret bounds for online convex minimization with only noisy function evaluations. Conceptually, if the LLM’s probability function _L_ ( _s_ ) were log-concave and the algorithmic cost _d_ ( _s_ ) convex, the target distribution _pτ_ ( _s_ ) _∝L_ ( _s_ ) _e_<sup>_−τd_(</sup><sup>_s_)</sup> would be log-concave, making it amenable to BCO techniques. Our framework extends this to the general scenario where the prior _L_ ( _s_ ) need not be log-concave, and the function _d_ ( _s_ ) need not be convex. We therefore need a somewhat weaker learnability condition that is applicable to these situations. 

**Bayesian Methods.** Coarse learnability is conceptually related to posterior-contraction results in Bayesian nonparametrics (Ghosal and van der Vaart, 2017; van der Vaart and van Zanten, 2008), which characterize how a Bayesian posterior concentrates around the true distribution with increasing data. Unlike those asymptotic consistency results, our assumption is a finite-sample condition ensuring that a learned generative model maintains sufficient mass on high-value regions during iterative optimization. Finally, our work bears superficial similarity to the use of Bayesian posteriors in guiding exploration (Srinivas et al., 2010; Russo and Van Roy, 2014). However, in those settings the posterior merely quantifies uncertainty and could be replaced by frequentist confidence bounds such as UCB. In contrast, in our framework the generative model is an integral component of the optimization process itself, progressively refining its distribution toward the optimal solution. 

## **2. Optimization Framework with a Generative Model** 

We consider the problem of minimizing a global objective function _d_ : _S →ℜ_ , where _S_ is the solution space.<sup>1</sup> As is standard in MCMC literature, we assume w.l.o.g. that _d_ ( _s_ ) _∈_ [0 _, D_ ] for all _s ∈ S_ . We assume only zeroth-order oracle access to _d_ ( _s_ ): we can evaluate _d_ ( _s_ ) for any _s ∈ S_ , but do not have access to its gradients. In our canonical applications (e.g., Section 9), _d_ ( _·_ ) can typically be computed efficiently by an algorithm. In addition, we assume access to a prior distribution _L_ ( _s_ ). This prior _L_ ( _s_ ) can be modeled by a generative distribution, such as that provided by parametrized or generative models. 

Our goal is to identify solutions _s_ that attain low values of _d_ ( _s_ ) while also having high probability under _L_ ( _s_ ). This objective can be formulated as sampling from, or finding the modes of, the target distribution: 

_pT_ ( _s_ ) _∝L_ ( _s_ ) _· e_<sup>_−T·d_(</sup><sup>_s_)</sup> _,_ 

where _T >_ 0 is a ‘temperature’ parameter that controls how sharply _pT_ ( _s_ ) concentrates on solutions _s_ that minimize _d_ ( _s_ ) among those with significant probability mass under _L_ ( _s_ ). 

This sampling problem is particularly interesting when the generative model _L_ is very unlikely to generate solutions with small _d_ ( _·_ ), and when a random solution _s_ with low _d_ ( _s_ ) is also very unlikely to have relatively high probability under _L_ compared to a carefully chosen _s_ . We assume that given samples from any distribution _D_ , we can use these samples to learn a distribution that is close to _D_ , for instance, via parameter-fitting. We will make the learning assumption more precise later, and this will be one of our key contributions. 

In the sequel, we use _s ∼L_ to denote that the sample _s_ is generated by a model _L_ . For distributions _P, Q_ , let _d_ tv( _P, Q_ ) denote the _total variation distance_ between them. 

> 1. In practice, _S_ is conditioned on the prompt string _x_ , which encodes the local and global constraints of the problem instance; we omit _x_ from the subsequent discussion. 

6 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

## **3. ALDRIFT: An Algorithm with Provable Guarantees** 

We now develop our algorithm ALDRIFT for solving the sampling problem above, with provable guarantees. Before presenting the algorithm, we first discuss a natural heuristic, TOPIFT, which highlights key technical challenges in obtaining formal bounds and thereby motivates both our algorithm and the assumptions underlying it. 

### **3.1. A Simple Heuristic: TOPIFT** 

To build intuition for why our sampling problem is non-trivial, we begin with a natural heuristic, TOPIFT, which iteratively refines the model by sampling from the current distribution, selecting the lowest-cost samples, and fitting a model to this elite set. Although effective empirically, TOPIFT highlights the challenges that motivate the principled algorithm, ALDRIFT (Section 3.2). 

At iteration _r_ , the heuristic draws _m · M_ samples from the current model _Lr−_ 1, evaluates the zeroth-order cost _d_ ( _s_ ) for each sample, selects the best _m_ samples, and learns _Lr−_ 1 using this set to obtain _Lr_ . The cost function _d_ ( _·_ ) thus _guides_ the refinement of the model in conjunction with the prior. 

**Algorithm 1:** TOPIFT: Iterated Fitting of Targets Using Top Samples. **Input:** _m, M, Q_ **Data:** _L_ (initial model) _L_ 0 _←L_ ; // initialize **for** _r ←_ 1 **to** _Q_ **do** sample _Sr_ from _Lr−_ 1 with _|Sr|_ = _m · M_ ; // generate samples evaluate _d_ ( _s_ ) for all _s ∈ Sr_ ; // compute cost _Sr_<sup>_′←m_samples in</sup><sup>_Sr_with smallest</sup><sup>_d_(</sup><sup>_s_) ;</sup> // elite set _Lr ←_ fit a model to the samples _Sr_<sup>_′_;</sup> // update model **end return** _LQ_ 

The heuristic in Algorithm 1 is closely related to the cross-entropy (CE) method (Rubinstein, 1999), where an “elite” set of high-performing samples is repeatedly used to update a parametric model via MLE. In our setting, the generative model plays the role of the parametric family, and model-fitting corresponds to the MLE update. However, CE-style updates are difficult to analyze, since the hard-min elite-selection step can induce mode collapse and eliminate coverage of important regions. 

These difficulties manifest directly in TOPIFT: Its hard-min selection step is analytically brittle, and repeated model-fitting without explicit control over density ratios can progressively erode probability mass on rare but critical regions. ALDRIFT resolves these issues by replacing hard-min with a controlled annealing schedule and by introducing Metropolis–Hastings corrections (Section 3.2), ensuring that samples at each iteration follow the correct intermediate target distribution; this prevents coverage errors from compounding across iterations. We present the connection between ALDRIFT and TOPIFT in more detail in Appendix A.1, and empirically demonstrate the need for iterated distribution correction in Section 6. 

To implement the Metropolis–Hastings correction and hence show our theoretical results, we require the following assumption. This assumption holds whenever the generative model admits 

7 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

tractable likelihood evaluation, including many autoregressive sequence models and open weight models. 

**Assumption 1** _For any s ∈ S, the probability value L_ ( _s_ ) _is available. This must hold not only for the initial model but also for any intermediate models obtained._ 

### **3.2. ALDRIFT Algorithm** 

Our final algorithm, ALDRIFT, is presented in Algorithm 2. The input to ALDRIFT is the number of samples ( _m_ = poly( _T, D_ )), and the parameter _T_ . We set _M_ = _m_<sup>2</sup> . Recall that _D_ = max _s∈S d_ ( _s_ ). 

In this algorithm, we intend the model _Lτ_ ( _s_ ) to be an approximation to _pτ_ ( _s_ ) _∝L_ ( _s_ ) _· e_<sup>_−τ·d_(</sup><sup>_s_)</sup> , where the temperature parameter _τ_ will gradually increase from 0 to _T_ . The main difference between ALDRIFT and TOPIFT is that the probability of retaining a sample is adjusted based on the target distribution _pτ_ . This adjustment is an interesting application of the Metropolis–Hastings algorithm (Metropolis et al., 1953), which runs the IMH chain for _M_ steps until mixing. We require Assumption 1 for both _L_ and the intermediate learned models _Lτ_ , in particular to enable MCMC sampling from _pτ_ given a model for _pτ_ -. As discussed in Section 4, this prevents errors in model learning from accumulating across iterations. We detail the necessity of Metropolis–Hastings sampling in Appendix A.2. 

**Remarks.** In Algorithm 2, we use a single complexity parameter _m_ to control multiple aspects of the algorithm for simplicity of analysis. As stated in Assumption 2, _m_ primarily serves as a learnability parameter, i.e., the number of samples required. We also use _m_ to determine both the number of Metropolis–Hastings iterations (running the step _m_ times) and the length of each iteration ( _M_ = _m_<sup>2</sup> ). This ensures that the computational effort per simulated annealing step scales polynomially with the learnability parameter. Further, in certain cases like the setting in Sections 5 and 6, the dependence of the run-time on _D_ can be removed via a geometric annealing schedule. We also note that the model-fitting step is efficient in practice if we use the parameters of _Lτ −_ as an efficient starting point to learn _Lτ_ , preventing the need to learn from scratch in each iteration. Finally, Algorithm 2 is an instance of Model Reference Adaptive Search (MRAS) (Hu et al., 2007), which generalizes the cross-entropy method (Rubinstein, 1999). We present this connection in Appendix A.3. 

## **4. Coarse Learnability and Sample Complexity of ALDRIFT** 

We will analyze the sample complexity of ALDRIFT in Section 4. To do this, we need an assumption on the learning agent. In Section 4, we propose the novel “coarse learnability” assumption, which essentially says that if we can approximately generate samples from _pτ_ , then we can coarsely learn a model _Lτ_ for it using the samples. Coarse learnability asks only that model fitting produce a proposal with tails heavy enough to cover the target up to polynomial density ratios (in the number of samples used) on all but exponentially rare target mass. 

For two distributions _p_ and _L_ on the same support _S_ , we define the _coverage_ of _L_ with respect to _<u>p</u>_ <u>(</u> _s_ <u>)</u> _p_ at a point _s ∈ S_ as cov _p,L_ ( _s_ ) = _L_ ( _s_ )<sup>_._This notion, similar to analogous notions in reinforcement</sup> learning and inference-time alignment (e.g., (Xie et al., 2023; Huang et al., 2025)), quantifies how well the proposal distribution _L_ “covers” the probability mass of the target _p_ : large values indicate under-coverage, while small values indicate over-coverage. 

8 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

**Algorithm 2:** ALDRIFT: Algorithm Driven Iterated Fitting of Targets. **Input:** _m, T_ **Data:** _L_ (base model), _D_ (temperature step denominator) _L_ 0 _←L τ ←_ 0 _M ← m_<sup>2</sup> ; // choice of _M_ justified in Theorem 1. **while** _τ ≤ T_ **do** _τ_ - _← τ_ ; _τ ←_ min � _τ_ + _D_<sup>1</sup><sup>_, T_</sup> �; _Sτ ←_ ∅; // initialize sample set at this temperature **for** _k ←_ 1 **to** _m_ **do** Sample _s_ 0 _∼Lτ_ -; _wτ_ ( _s_ 0) _←L_ ( _s_ 0) _· e_<sup>_−τ·d_(</sup><sup>_s_0)</sup> ; // _τ_ - is the previous value of _τ_ **for** _i ←_ 1 **to** _M_ **do** Sample ˆ _si ∼Lτ_ -; _wτ_ (ˆ _si_ ) _←L_ (ˆ _si_ ) _· e_<sup>_−τ·d_(ˆ</sup><sup>_si_)</sup> ; // weight; note _pτ_ ( _s_ ) _∝ wτ_ ( _s_ ) _βi ←_ min 1 _,_<sup>_wτ_</sup><sup><u>(</u></sup><sup>_s_ˆ</sup><sup>_i_</sup><sup><u>)</u></sup> ; // MH acceptance probability � _Lτ_ -(ˆ _si_ )<sup>_·L_</sup> _w_<sup>_τ_</sup> _τ_<sup>-</sup> (<sup><u>(</u></sup> _s_<sup>_s_</sup> _i_<sup>_i_</sup> _−_<sup>_−_</sup> 1<sup>1</sup> )<sup><u>)</u></sup> � **if** _u ∼_ Uniform(0 _,_ 1) _satisfies u ≤ βi_ **then** _si ← s_ ˆ _i_ **else** _si ← si−_ 1 **end end** _Sτ ← Sτ ∪{ sM }_ ; // append final sample into multiset of samples **end** _Lτ ←_ fit a model to the samples _Sτ_ ; // _Lτ_ is the learned model for _pτ_ **end return** _LT_ 

9 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

**Assumption 2 (Coarse Learnability)** _For each temperature τ ∈_ [0 _, T_ ] _, let pτ_ ( _s_ ) _∝L_ 0( _s_ ) _·e_<sup>_−τd_(</sup><sup>_s_)</sup> _be the target distribution and Lτ the model obtained after fitting. We say the model family satisfies_ coarse learnability _if for any large enough K ≥_ poly( _D, T_ ) _and any error ε ∈_ (0 _,_ 1) _and confidence δ ∈_ (0 _,_ 1) _, there is a sample size m_ = poly( _K/δ,_ ln 1 _/ε_ ) _such that the following holds:_ 

_If Lτ is trained using m samples from a distribution p_ ˆ _, then with probability at least_ 1 _− δ (over the training samples), the learned model satisfies:_ 



The key distinction between Assumption 2 and standard density estimation or PAC learning (Valiant, 1984) lies in the error regime. Standard guarantees typically yield error rates polynomial in the sample size ( _ε ≈_ poly(1 _/m_ )). In contrast, our sample complexity _m_ scales with ln(1 _/ε_ ), which means polynomial samples yield _exponentially small_ error probabilities ( _ε ≈ e_<sup>_−m_</sup> ), albeit for a coarse coverage guarantee. This stronger tail bound requirement is not a technical artifact but a necessity for optimization. Since we assumed the global optimum could have exponentially small probability under the initial prior, a learner with only polynomial error guarantees could validly assign vanishing probability to the optimal region. The exponential tail bound ensures that the intermediate models preserve coverage of these rare regions throughout the annealing schedule. 

To build intuition, we consider the following simplification. Assume _p_ ˆ = _pτ_ . For given _K_ , set _ε_ = _e_<sup>_−K_</sup> and _δ_ = 1 _/K_ . Assumption 2 now implies _K_ = _m_<sup>_β_</sup> for some constant _β ∈_ (0 _,_ 1). If we re-parametrize in terms of _m_ , we have _ε_ = _e_<sup>_−mβ_</sup> . In this regime, _K ≤ m_ , so that we can use _m_ instead of _K_ in Eq. (1), which yields Pr [cov _pτ ,Lτ_ ( _s_ ) _> m_ ] _≤ ε_ = _e_<sup>_−mβ_</sup> _._ Then, Assumption 2 simplifies to the following property for general parametric models and targets: 

**Assumption 2, special case.** A model _L_ coarsely learns a parametric distribution _p_ if for sufficiently large sample size _m_ that depends polynomially on the parameters of the distribution, w.p. 1 _−_ 1 _/m_<sup>_β_</sup> , the model _L_<sup>_m_</sup> trained on _m_ samples from _p_ satisfies Pr [cov _p,Lm_ ( _s_ ) _> m_ ] _≤ e_<sup>_−mβ_</sup> , where _β >_ 0 is a small constant. 

Coarse learnability guarantees polynomial coverage of the target density, except on an atypical set of exponentially small measure. Unlike density estimation guarantees that require the total variation distance to vanish, this condition allows for persistent approximation errors (model misspecification; see Section 7.1). This extends coverage-based analyses (Huang et al., 2025) to the iterative setting, where as long as the coverage remains polynomially bounded, the M-H correction can recover the exact target distribution, bridging regimes where the initial coverage gap is exponentially large via intermediate polynomial steps. While this appears to be a strong assumption, such intuition is implicit in classical MBO (Rubinstein, 1999; Hu et al., 2007), and is fundamentally linked to statistical estimators that prioritize heavy tails (e.g., over-smoothed KDE). In Section 6, we empirically demonstrate a non-convex optimization setting where an inflated proposal with distribution correction are necessary for the global convergence of ALDRIFT when sample budgets are small. In Section 7, we provide evidence supporting the plausibility of Assumption 2 for wellknown generative distributions. 

Our main analytical result analyzes the sample complexity of ALDRIFT under coarse learnability. 

10 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

**Theorem 1** _Under Assumption 2, for sufficiently large m_ = _poly_ ( _T, D_ ) _the sample complexity of_ ALDRIFT _is O_ ( _mMTD_ ) = poly( _T, D_ ) _, and with high probability, the sampling distribution p_ ˆ _of ST satisfies_<sup>2</sup> _d_ tv(ˆ _p, pT_ ) = _O_ � _e_<sup>_−mα_�</sup> _, where α >_ 0 _is a constant._ 

### **4.1. Proof of Theorem 1** 

Our proof focuses on a particular iteration _τ >_ 0. We consider the inner loops of ALDRIFT, where we generate the set of samples _Sτ_ using Metropolis-Hastings. Let _Wτ −_ = _{s | pτ −_ ( _s_ ) _≤ m · Lτ −_ ( _s_ ) _}_ be the “typical set” where the proposal covers the previous target, and let _η_ = Pr _pτ −_ [ _Wτ_<sup>_c−_]</sup> be the mass of the atypical set. 

**Lemma 2** _At step τ , let E be the event that the Metropolis-Hastings chain in_ ALDRIFT _encounters a state s ∈ Wτ_<sup>_c−at any step during the generation of the m samples in Sτ.With probability at least_</sup> 1 _− m_<sup>2</sup> _η, the event E does not occur. Conditioned on ¬E, the distribution p_ ˆ _of any sample generated by the chain satisfies:_ 







The algorithm takes _M_ = _m_<sup>2</sup> steps per sample, for a total of _m_ samples. By a union bound over all these steps, the probability that a state in _Wτ_<sup>_c_</sup> -<sup>is ever proposed is at most</sup><sup>_m_3</sup><sup>_·_(</sup><sup>_η/m_) =</sup><sup>_m_2</sup><sup>_η_.This</sup> establishes the probability bound for event _E_ . 

Conditioned on _¬E_ , the chain operates entirely within _Wτ_ -. Since _pτ_ ( _s_ ) _∝ pτ_ -( _s_ ) _e_<sup>_−d_(</sup><sup>_s_)</sup><sup>_/D_</sup> and since _d_ ( _s_ ) _∈_ [0 _, D_ ] for all _s_ , this means _pτ_ ( _s_ ) _≤ e · pτ −_ ( _s_ ). Thus, for any _s ∈ Wτ_ -, the density ratio with respect to the _new_ target is bounded: 



The sampling procedure is therefore equivalent to an independent Metropolis–Hastings (IMH) chain restricted to _Wτ_ - with density ratio bounded by _em_ . By the uniform ergodicity of IMH (Mengersen and Tweedie, 1996; Tierney, 1994), the variation distance to the restricted target _p_<sup>_′_</sup> _τ_<sup>_∝pτ|W_</sup> _τ −_<sup>after</sup> _M_ = _m_<sup>2</sup> steps is: 



We finally bound the distance to the true target _pτ_ . The error introduced by restricting the target to _Wτ_ - is bounded by the mass of the excluded set under _pτ_ : 



By the triangle inequality: 



> 2. Since _pτ_ is only coarsely learnable via _Lτ_ , we need to consider the _d_ tv with respect to the sampling distribution _Sτ_ , which corrects this coarse learning error via the Metropolis–Hastings procedure. 

11 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

This completes the proof. 

Using the above lemma, we now complete the proof of Theorem 1. **Proof** [Proof of Theorem 1] As in the text following Assumption 2, we set _ε_ = exp( _−K_ ) and _δ_ = 1 _/K_ , so that _K_ = _m_<sup>_β_</sup> for constant _β >_ 0. We now choose _m_ large enough that _m_<sup>_β_</sup> = _ω_ ( _TD_ ), and note that _m ≥ K_ . 

We prove by induction that if the algorithm succeeds (does not hit atypical sets), then for all _τ_ , _d_ tv(ˆ _p, pτ_ ) = _O_ ( _e_<sup>_−mα_</sup> ) for some constant _α ∈_ (0 _, β_ ). For the base case, note that _d_ tv(ˆ _p, p_ 0) = 0 since we begin with the model _L_ 0 = _L_ . For the inductive step, assume _d_ tv(ˆ _p, pτ −_ ) _≤ ε_ prev. By Assumption 2, the learned model _Lτ −_ has an atypical set mass _η ≤ O_ ( _ε_ prev) + _e_<sup>_−mβ_</sup> . Applying Lemma 2, the error at the next step is: 



Unrolling this recurrence over _T · D_ steps results in an error growth of _ϕ_<sup>_TD_</sup> for some constant _ϕ >_ 1. Thus: 



Assuming _m_<sup>_β_</sup> = _ω_ ( _TD_ ), we have _d_ tv(ˆ _p, pT_ ) = _O_ ( _e_<sup>_−mα_</sup> ). This completes the induction. 

The algorithm fails at any step _τ_ if (a) learning fails (probability _δ_ ) or (b) sampling hits _W_<sup>_c_</sup> (probability _m_<sup>2</sup> _· η_ ). The above derivation yields _η_ = _O_ ( _e_<sup>_−mα_</sup> ), so that we have _m_<sup>2</sup> _η_ = _o_ � _m_<sup>_−β_�</sup> . Further, _δ_ = 1 _/K_ = _m_<sup>_−β_</sup> . By a union bound over _T · D_ steps, total failure probability is _O_ ( _T · D · m_<sup>_−β_</sup> ) = _o_ (1) since we assume _m_<sup>_β_</sup> = _ω_ ( _TD_ ). 

Finally, at given any _τ_ , the total number of samples is _O_ ( _m_<sup>3</sup> ) = poly( _T, D_ ). This completes the proof of Theorem 1. 

## **5. Sample Complexity of ALDRIFT for Bounded Non-Convex Optimization** 

Classical zeroth-order global optimization in R<sup>_n_</sup> often relies on local Markov Chain Monte Carlo (MCMC) methods (Kalai and Vempala, 2006). While these methods achieve polynomial time complexity on strictly log-concave target distributions, they can require exponential time to mix on non-convex landscapes due to local energy barriers (Holley and Stroock, 1987; Hajek, 1988). We prove that Model-Based Optimization (MBO) overcomes this limitation, and achieves logarithmic sample complexity in the precision parameter, hence providing a finite-sample analog to the asymptotic convergence results for MRAS. 

By leveraging a modification of ALDRIFT with an inflated proposal distribution _Lτ_ , we show that it can efficiently (globally) optimize non-convex functions that are bounded by a quadratic envelope. In particular, we show that Assumption 2 holds at all intermediate steps with a bound _K_ that is independent of the temperature parameter _τ_ , guaranteeing sample complexity _O_<sup>�</sup> (log 1 _/ε_ ) to achieve error _ε_ in the global optimum, matching the bounds of space partitioning methods (Munos, 2011; Bubeck et al., 2011) for this setting (under some caveats that we mention in Section 5.4). The _O_ ( _·_ ) notation hides constants that depend on _n, K_ , and log<sup><u>1</u></sup> _δ_<sup>.</sup> 

Complementing this theoretical result, in Section 6, we present an empirical demonstration of the need for an inflated proposal distribution (with sample correction) in ensuring the convergence of ALDRIFT with limited sample budgets, comparing it to TOPIFT that uses the empirical variance and samples without distribution correction, and gets trapped in local optima. 

12 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

### **5.1. Optimization Setting and Algorithm** 

The domain is R<sup>_n_</sup> . Assume the generative prior is a Gaussian _L_ 0( _x_ ) _∝_ exp( _−U_ ( _x_ )), where _U_ ( _x_ ) =<sup>_<u>µ</u>_</sup> 2<sup><u>0</u></sup><sup>_∥x −x_0</sup><sup>_∥_2 for some</sup><sup>_µ_0</sup><sup>_>_0.</sup> 

Assume the objective _d_ ( _x_ ) has a unique global minimum at _x_<sup>_∗_</sup> . We assume _d_ ( _x_ ) is bounded by a quadratic envelope around its true optimum: there exist constants _µd, Ld >_ 0 such that for all _x ∈_ R<sup>_n_</sup> , 



Note that _d_ ( _x_ ) is not assumed to be convex and may contain arbitrary local non-convexities within these bounds. This model is well-studied in non-convex optimization; see for instance (Munos, 2011; Bubeck et al., 2011). 

We now run ALDRIFT for _N_ steps as described in Section 5.3. There are changes needed to the algorithm to handle the lack of an upper bound on _d_ ( _x_ ), and to make the sampling process exact, that we detail there. We also detail the parameter settings there, and re-do the proof of sample complexity. 

When the temperature parameter is _τ_ , the target distribution is _pτ_ ( _x_ ) _∝_ exp( _−fτ_ ( _x_ )), where _fτ_ ( _x_ ) = _U_ ( _x_ ) + _τd_ ( _x_ ). The algorithm draws _m_ samples from _pτ_ (where the parameter _m_ will be chosen later), computes the empirical mean _ω_ ˆ _τ_ , and fits the proposal distribution (or generative model) _Lτ_ ( _x_ ) = _N_ (ˆ _ωτ , µ_<sup><u>2</u></sup> _τ_<sup>_In_),where</sup><sup>_µτ_=</sup><sup>_µ_0+</sup><sup>_τµd_.Weassumethesamplingisexactlyfrom</sup> _pτ_ , and we justify this in Section 5.3. It is also crucial for our proof of Theorem 3 below that the distribution has larger variance than desired and is set based on the convex envelope parameters _µd, Ld_ , hence deviating from standard MBO that uses the sample variance directly. 

### **5.2. Verifying Coarse Learnability** 

We now show that Assumption 2 holds at all intermediate steps of the algorithm, for the proposal distribution _Lτ_ ( _x_ ) = _N_ (ˆ _ωτ , µ_<sup><u>2</u></sup> _τ_<sup>_In_).Note that in this setting,Assumption 2 is not an assumption;</sup> we show that it holds because of our choice of the model _Lτ_ ( _x_ ). To simplify presentation, we define the following global geometric constants: 



- The inflation factor: _B_ = _κ_<sup>_n/_</sup> max<sup>2exp(</sup><sup>_E_</sup> shift<sup>).</sup> 

We will further assume in the rest of the section that _d_ ( _x_<sup>_∗_</sup> ) = 0, so that _d_ ( _x_ ) _≥_ 0 for all _x_ . This is w.l.o.g., since the normalized density _pτ_ remains unchanged if we replace _d_ ( _x_ ) with _d_ ˜( _x_ ) = _d_ ( _x_ ) _− d_ ( _x_<sup>_∗_</sup> ), so that the algorithm’s execution remains identical. 

**Theorem 3 (Coarse Learnability of** _pτ_ **)** _Given the setting and algorithm defined above, if the perstep sample size satisfies m ≥ C_ � _<u>n</u>_ 2<sup>ln</sup><sup>_κ_max +</sup><sup>_Eshift_</sup> �� _n_ + ln<sup>_<u>N</u>_</sup> _δ_ � _for constant C >_ 0 _, then the_ 

13 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

_model pτ globally satisfies the following condition_<sup>3</sup> _with probability at least_ 1 _− δ/_ (2 _N_ ) _:_ 



**Remarks.** Theorem 3 can be viewed as a special case of the Coarse Learnability assumption (Assumption 2). Because Theorem 3 establishes a global supremum bound on the density ratio, we have Pr[ratio _> K_ ] = 0. Furthermore, because we utilize Rejection Sampling (Section 5.3), the empirical samples are drawn perfectly from the target, meaning _d_ tv(ˆ _p, pτ_ ) = 0. Consequently, the inequality in Assumption 2 is satisfied for any _ε >_ 0. Further, the sample complexity is _m_ = poly (ln _K,_ ln 1 _/δ_ ), which is stronger than the bound in Assumption 2, assuming _K_ is a large enough function of the problem parameters (but independent of _T_ ). Theorem 3 suffices for the specialized analysis of ALDRIFT that we perform in Section 5.3. 

Note that _K_ (and consequently the algorithm’s sample complexity) does not grow with _τ_ . This non-asymptotically captures the limiting behavior predicted by Laplace’s method (Wong, 2001) and the Bernstein-von Mises theorem (Vaart, 1998) in Bayesian inference: as the _τ_ -scaled regularizer overwhelms the prior, the prior collapses into a constant spatial penalty evaluated at the optimum. However, while those classical theorems are valid only as _τ →∞_ , our quadratic envelope technique provides an upper bound for any finite _τ ≥_ 0. 

The rest of this subsection is devoted to proving this theorem. 

**Upper Bounding** _pτ_ **.** We now show a sequence of lemmas that will bound the density ratio. We start with _pτ_ , and bound it via standard methods. 

**Lemma 4 (Target Envelope)** _The target distribution pτ_ ( _x_ ) _is globally upper-bounded by a scaled Gaussian envelope:_ 



_where x_ ¯ _τ_ =<sup>_<u>µ</u>_</sup><sup><u>0</u></sup><sup>_x_</sup><sup><u>0+</u></sup><sup>_τ_</sup><sup>_<u>µdx∗</u>_</sup> _. µτ_ 

**Proof** Let the target probability distribution be defined as _pτ_ ( _x_ ) = _Z_ <u>1</u> _τ_<sup>exp(</sup><sup>_−fτ_(</sup><sup>_x_)), where</sup><sup>_fτ_(</sup><sup>_x_) =</sup> _<u>µ</u>_ 20<sup>_∥x −x_0</sup><sup>_∥_2 +</sup><sup>_τd_(</sup><sup>_x_) and</sup><sup>_Zτ_=</sup> �R<sup>_n_exp(</sup><sup>_−fτ_(</sup><sup>_x_))</sup><sup>_dx_is the normalizing constant.</sup> By assumption, _d_ ( _x_ ) is bounded by quadratics: _<u>µ</u>_ 2 _<u>d</u>_<sup>_∥x −x∗∥_2</sup><sup>_≤d_(</sup><sup>_x_)</sup><sup>_≤L_</sup> 2<sup>_<u>d</u>∥x −x∗∥_2.We</sup> can therefore sandwich _fτ_ ( _x_ ) between a lower bounding quadratic _fτ,_ low( _x_ ) and an upper bounding quadratic _fτ,_ up( _x_ ): 



We first simplify _fτ,_ low( _x_ ) as follows: 



> 3. This condition is slightly different from how Assumption 2 is phrased, but suffices for the sample complexity proof in Section 5.3. 

14 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

To consolidate this into a single quadratic, we define _µτ_ = _µ_ 0 + _τµd_ and the weighted center _x_ ¯ _τ_ =<sup>_<u>µ</u>_</sup><sup><u>0</u></sup><sup>_x_</sup><sup><u>0+</u></sup><sup>_τ_</sup><sup>_<u>µdx∗</u>_</sup> . Substituting these into the expansion yields: _µτ_ 

where 



Analogously, substituting _µd_ with _Ld_ , completing the square for _fτ,_ up( _x_ ) yields a quadratic with smoothness _Lτ_ = _µ_ 0 + _τLd_ , centered at _x_ ˜ _τ_ =<sup>_<u>µ</u>_</sup><sup><u>0</u></sup><sup>_x_</sup><sup><u>0+</u></sup><sup>_τLdx∗_</sup> : _µ_ 0+ _τLd_ 



Observe now that the fractional term in _Cτ,_ up: 



Thus, for all _τ ≥_ 0: 



Since _Cτ,_ low _≥_ 0, we have: 



Since _fτ_ ( _x_ ) _≤ fτ,_ up( _x_ ) for all _x_ , it follows that exp( _−fτ_ ( _x_ )) _≥_ exp( _−fτ,_ up( _x_ )). We now lower-bound the normalizer _Zτ_ as: 



15 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

The remaining integral is an unnormalized multivariate Gaussian with covariance matrix Σ = _L_ <u>1</u> _τ_<sup>_I_.Since</sup> � exp( _−_<sup><u>1</u></sup> 2<sup>_xT_Σ</sup><sup>_−_1</sup><sup>_x_)</sup><sup>_dx_=</sup> ~~�~~ (2 _π_ )<sup>_n_</sup> det(Σ), we get: 



We finally upper-bound the numerator of _pτ_ ( _x_ ) as: _fτ_ ( _x_ ) _≥ fτ,_ low( _x_ ) = _⇒_ exp( _−fτ_ ( _x_ )) _≤_ exp( _−fτ,_ low( _x_ )). Applying this to the numerator and dividing by our lower bound for _Zτ_ : 



Since _Lτ /µτ ≤ κ_ max, we can bundle the leading factors into a single constant _B_ = _κ_ max<sup>_n/_2</sup><sup>_eE_shift,</sup> yielding the final bound: 



This completes the proof. 

The previous lemma immediately yields the following corollary: 

**Corollary 5** _The normalizer Zτ is bounded as:_ 



_In particular, the ratio between these bounds is:_ 



**Sub-Gaussian Upper Bound.** Let _q_ ( _x_ ) = _N_ (¯ _xτ , µ_<sup><u>1</u></sup> _τ_<sup>_In_).FromTheorem4,wehave:</sup><sup>_pτ_(</sup><sup>_x_)</sup><sup>_≤_</sup> _B · q_ ( _x_ ). We now have the following lemmas using this inequality, which will help us bound the density ratio. We provide the proof of the lemma below for completeness. 

**Lemma 6** _Let ω_ ˜ _τ_ = E _pτ_ [ _x_ ] _be the true expectation. Then,_ 



16 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

**Proof** By Jensen’s inequality, _∥ω_ ˜ _τ − x_ ¯ _τ ∥_<sup>2</sup> _≤_ E _pτ_ [ _∥x − x_ ¯ _τ ∥_<sup>2</sup> ]. Let _z_ =<sup>_√_</sup> _<u>µτ</u>_ <u>(</u> _x − x_ ¯ _τ_ ). Under the proposal distribution _q_ , _z ∼N_ (0 _, In_ ), which we denote by _ϕ_ ( _z_ ). Under the target distribution, _z_ follows some density _p_ ( _z_ ). Since _z_ and _x_ are linearly related, we have _p_ ( _z_ ) _≤ Bϕ_ ( _z_ ). We seek to bound E _p_ [ _∥z∥_<sup>2</sup> ]. Since _p_ ( _z_ ) _≤ Bϕ_ ( _z_ ), the Kullback-Leibler divergence is bounded: 



By the Donsker-Varadhan representation Boucheron et al. (2013), for any measurable function _f_ ( _z_ ) and any _λ >_ 0: 



We choose _f_ ( _z_ ) = _∥z∥_<sup>2</sup> . Under _ϕ_ ( _z_ ), _∥z∥_<sup>2</sup> follows a _χ_<sup>2</sup> _n_<sup>distribution, whose moment generating</sup> function is E _ϕ_ [ _e_<sup>_λ∥z∥_2</sup> ] = (1 _−_ 2 _λ_ )<sup>_−n/_2</sup> for _λ <_ 1 _/_ 2. Substituting this and our KL bound yields: 











Replacing _z_ with<sup>_√_</sup> _<u>µτ</u>_ <u>(</u> _x − x_ ¯ _τ_ ) concludes the proof. 

Before proceeding, we formally define the _variance proxy_ of a sub-Gaussian random variable (Vershynin, 2018). A random variable _Z_ with mean _µZ_ is sub-Gaussian with variance proxy _ν_<sup>2</sup> if _Z_ satisfies the tail bound Pr( _|Z − µZ| ≥ t_ ) _≤_ 2 exp( _−t_<sup>2</sup> _/ν_<sup>2</sup> ) for all _t ≥_ 0. A random vector _X ∈_ R<sup>_n_</sup> is sub-Gaussian with variance proxy _ν_<sup>2</sup> if its one-dimensional projections _⟨X − µX , u⟩_ onto any unit vector _u ∈_ S<sup>_n−_1</sup> are sub-Gaussian with variance proxy _ν_<sup>2</sup> . The following lemma is now straightforward (see (Vershynin, 2018)). 



We will need the following concentration bound; see (Vershynin, 2018) for a proof. 

**Lemma 8 (Empirical Mean of Sub-Gaussian Vectors)** _Let X_ 1 _, . . . , Xm be independent, identically distributed random vectors in_ R<sup>_n_</sup> _with mean ω_ = E[ _X_ 1] _. Assume each Xi is sub-Gaussian with variance proxy ν_<sup>2</sup> _. Let ω_ ˆ = _m_<sup><u>1</u></sup> � _mi_ =1<sup>_Xibe the empirical mean.Then, there exists a constant_</sup> _C >_ 0 _such that for any t >_ 0 _, with probability at least_ 1 _− e_<sup>_−t_</sup> _:_ 



17 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

**Proof of Theorem 3.** Using these ingredients, we now prove Theorem 3. **Proof** [Proof of Theorem 3] We evaluate the density ratio _rτ_ ( _x_ ) = _pτ_ ( _x_ ) _/Lτ_ ( _x_ ). The proposal generative model is _Lτ_ ( _x_ ) = _N_ (ˆ _ωτ , µ_<sup><u>2</u></sup> _τ_<sup>_In_) with density (</sup><sup>_<u>µ</u>_</sup> 4 _π_<sup>_<u>τ</u>_)</sup><sup>_n/_2 exp(</sup><sup>_−_</sup><sup>_<u>µ</u>_</sup> 4<sup>_<u>τ</u>∥x −ω_ˆ</sup><sup>_τ∥_2).Using the</sup> upper bound from Theorem 4 for the numerator: 



We apply triangle inequality: _∥x − ω_ ˆ _τ ∥_<sup>2</sup> _≤_ 2 _∥x − x_ ¯ _τ ∥_<sup>2</sup> + 2 _∥ω_ ˆ _τ − x_ ¯ _τ ∥_<sup>2</sup> to the second term in the exponent. The _x_ -dependent terms cancel and we have: 



By the triangle inequality, _∥ω_ ˆ _τ − x_ ¯ _τ ∥_<sup>2</sup> _≤_ 2 _∥ω_ ˆ _τ − ω_ ˜ _τ ∥_<sup>2</sup> + 2 _∥ω_ ˜ _τ − x_ ¯ _τ ∥_<sup>2</sup> . The exponent in the above expression is therefore bounded by _µτ ∥ω_ ˆ _τ − ω_ ˜ _τ ∥_<sup>2</sup> + _µτ ∥ω_ ˜ _τ − x_ ¯ _τ ∥_<sup>2</sup> . From Theorem 6, we have _µτ ∥ω_ ˜ _τ − x_ ¯ _τ ∥_<sup>2</sup> _≤_ 2 _n_ + 4 ln _B_ . 

To bound _µτ ∥ω_ ˆ _τ − ω_ ˜ _τ ∥_<sup>2</sup> , note that _ω_ ˆ _τ_ is the empirical mean of _m_ i.i.d. draws from the target distribution _pτ_ , while _ω_ ˜ _τ_ is the true mean. By Theorem 7, these independent draws from _pτ_ are sub-Gaussian random vectors with a variance proxy bounded by: 



for some constant _C_ sg _>_ 0. We now apply Theorem 8. Setting the failure probability to _e_<sup>_−t_</sup> = 2 _<u>δN</u>_<sup>,</sup> which implies _t_ = ln � <u>2</u> _δN_ �, we obtain with probability at least 1 _−_ 2 _<u>δN</u>_<sup>:</sup> 



so that 



To satisfy our requirement that _µτ ∥ω_ ˆ _τ − ω_ ˜ _τ ∥_<sup>2</sup> _≤_ 1, we set: 



where _C_<sup>_′_</sup> = _C · C_ sg. Therefore with probability at least 1 _−_ 2 _<u>δN</u>_<sup>,wehave</sup><sup>_<u>µ</u>_</sup> 2<sup>_<u>τ</u>∥ω_ˆ</sup><sup>_τ−x_¯</sup><sup>_τ∥_2</sup><sup>_≤_</sup> 1 + 2 _n_ + 4 ln _B_ . Substituting this into Eq. (3) yields the bound on _K_ . 

18 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

### **5.3. Implementing ALDRIFT via Geometric Annealing and Rejection Sampling** 

Given that we have a simple analytic generative model, we make two changes that both simplify ALDRIFT and lead to an exponentially improved sample complexity. Further note that we did not assume an upper bound on _d_ ( _x_ ) in this setting, which needs a different approach than Theorem 1. 

In the description below, we set the number of generated samples _m_ for each temperature from the statement of Theorem 3. 

- **Geometric Annealing.** We use a _geometric schedule_ of temperatures _τ_ . In particular, we set _τ_ 0 = 0, _τ_ 1 = _L_<sup>_<u>µ</u>_</sup><sup><u>0</u></sup> _d_<sup>, and</sup><sup>_τk_+1=(1 +</sup><sup>_γ_)</sup><sup>_· τk_for</sup><sup>_k≥_1, where</sup><sup>_γ_=1</sup><sup>_/n_.Since</sup><sup>_τN≥T_, this implies</sup> the number of outer iterations of ALDRIFT (temperature settings) is _N_ = _O n_ ln<sup>_TLd_</sup> . � _µ_ 0 � 

- Such a geometric schedule not only improves the dependence on _T_ exponentially, but is also robust to _d_ ( _x_ ) being unbounded. 

- **Rejection Sampling.** In the inner loop, to generate _m_ samples from _pτk_ +1, we use rejection sampling instead of Metropolis-Hastings. Though we don’t know the normalizing constant (which necessitated M-H in Section 3.2), we now have an upper bound from Theorem 5. Let 



At each sampling step, we generate a sample from _Lτk_ and accept with probability 



To generate a sample, we run this process for at most _ts_ = 10 _KB_<sup>2</sup> ln<sup><u>2</u></sup><sup>_<u>Nm</u>_</sup> _δ_ steps, declaring failure if a sample is not generated. We generate _m_ samples and use them to fit _Lτk_ +1. 

**Remark.** The above implementation requires _B_ is known, which implicitly assumes access to a loose upper bound _R ≥∥x_ 0 _− x_<sup>_∗_</sup> _∥_<sup>2</sup> . If such a bound is unavailable, we can use a standard doubling trick on _R_ to implement the sampling, where we start with _R_ = _ε_ and keep doubling _R_ whenever the sampling process fails. 

Focusing just on _T_ and ignoring the problem-dependent parameters of _B, n, K_ , the total sample complexity is therefore _O_<sup>˜</sup> (ln _T · m_ ) = _O_<sup>�</sup> �ln _T ·_ ln<sup>_<u>N</u>_</sup> _δ_ � = _O_<sup>�</sup> �ln _T ·_ ln<sup><u>ln</u></sup> _δ_<sup>_<u>T</u>_</sup> �, and we show below that the algorithm fails with probability at most _δ_ . 

### 5.3.1. ANALYSIS OF THE SAMPLING STEP 

We first show that the rejection sampling step is feasible, meaning that the accept probability is at most one. Clearly, if this is true, this process will generate _m_ unbiased samples from _pτk_ +1. 

**Lemma 9** _Let τ_<sup>_′_</sup> := _τk_ +1 _and τ_ = _τk and let γ be the multiplicative growth rate of the annealing procedure. Then, for all iterations k ≥_ 0 _, with probability_ 1 _−_ 2 _<u>δN</u>_<sup>_, we have:_</sup> 



_<u>pτ</u> ′_ <u>(</u> _x_ <u>)</u> _Consequently, setting the geometric rate to γ_ = _n_<sup><u>1</u></sup><sup>_yields_sup</sup><sup>_x_</sup> _Lτ_ ( _x_ )<sup>_≤B · K · √_</sup> _<u>e.</u>_ 

19 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

**Proof** We decompose the density ratio into two terms: 



From Theorem 3, we already know that with probability 1 _−_ 2 _<u>δN</u>_<sup>, we have</sup><sup>_r_(</sup><sup>_x_)</sup><sup>_≤K_for all</sup><sup>_x_.</sup> To bound the first term, we expand the target densities: 



By definition, _fτ ′_ ( _x_ ) _− fτ_ ( _x_ ) = ( _τ_<sup>_′_</sup> _− τ_ ) _d_ ( _x_ ). Because _τ_<sup>_′_</sup> _> τ_ and _d_ ( _x_ ) _≥_ 0, the exponential term is upper-bounded by 1. Therefore, the ratio of the densities is bounded as: 



We now bound the ratio _Zτ /Zτ ′_ using the bounds established in Theorem 5. For the numerator, we have 



where the last inequality follows because _Cτ,_ low _≥_ 0. For the denominator, we have: 



where we recall from Theorem 4 that _Cτ ′,_ up _≤ E_ shift. Therefore: 



We first assume _k ≥_ 1. We substitute the definitions _Lτ ′_ = _µ_ 0 + _τ_<sup>_′_</sup> _Ld_ and _µτ_ = _µ_ 0 + _τµd_ , along with the geometric schedule _τ_<sup>_′_</sup> = (1 + _γ_ ) _τ_ : 



where the last inequality follows since _κ_ max _≥_ sup _τ_ ( _Lτ /µτ_ ). Plugging this back into the partition function ratio gives: 



Substituting this back into Eq. (4) and multiplying by the second term _r_ ( _x_ ) _≤ K_ , we have: 



20 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

When _k_ = 0, note that _τ_ = 0 and _τ_<sup>_′_</sup> = _µ_ 0 _/Ld_ , so that 



Repeating the above argument completes the proof. Note that setting _γ_ = _n_<sup><u>1</u>yields the bound:</sup> 



This justifies the use of<sup>_√_</sup> _<u>eKB</u>_ as the bounding constant in the rejection sampling step. 

The previous lemma implies the accept probability in rejection sampling is at most one. We now bound the sampling steps needed to generate an accepted sample. 

**Lemma 10** _In any sampling step, the probability of acceptance is at least_ _~~√~~_ _<u>eB</u>_ <u>1</u><sup>2</sup> _K_<sup>_.Therefore,the_</sup> _probability that the sampling process ever fails over the entire course of the algorithm is at most δ._ 

**Proof** We use the definitions in Theorem 5, and the bound there as: 



Since the rejection process follows a geometric distribution, the probability a sample is not generated in _ts_ steps is at most 2 _Nmδ_<sup>, which when summed over</sup><sup>_N· m_total samples across all temperatures</sup> yields a failure probability of at most _δ/_ 2. Note that in Theorem 9, there is a probability _δ/_ (2 _N_ ) per temperature that the density ratio itself is not bounded. Taking the union bound over all such bad events yields a total failure probability of at most _δ_ . 

### 5.3.2. RELATING TEMPERATURE TO THE PRECISION OF GLOBAL OPTIMIZATION 

We now find the _T_ needed to achieve precision E _pT_ [ _d_ ( _x_ )] _≤ ε_ for a given _ε_ , hence casting our sample complexity in more standard terms. Recall we assumed _d_ ( _x_<sup>_∗_</sup> ) = 0. 

**Lemma 11 (Precision Scaling)** _To achieve an expected objective error_ E _pT_ [ _d_ ( _x_ )] _≤ ε, it suffices to set the final temperature to T_ = _O_ (1 _/ε_ ) _. This implies an overall sample complexity of O_ �(log 1 _/ε_ ) _._ **Proof** Since _d_ ( _x_ ) _≤_<sup>_L_</sup> 2<sup>_<u>d</u>∥x −x∗∥_2, taking the expectation over the final target distribution</sup><sup>_pT_(</sup><sup>_x_):</sup> E _pT_ [ _d_ ( _x_ )] _≤_<sup>_Ld_</sup> 2<sup>E</sup><sup>_pT_[</sup><sup>_∥x −x∗∥_2]</sup><sup>_≤Ld_E</sup><sup>_pT_[</sup><sup>_∥x −x_¯</sup><sup>_T ∥_2] +</sup><sup>_Ld∥x_¯</sup><sup>_T−x∗∥_2</sup><sup>_,_</sup> 

where we have used the triangle inequality. The second term expands to: 



To bound the term E _pT_ [ _∥x − x_ ¯ _T ∥_<sup>2</sup> ], we utilize Theorem 6: 



For sufficiently large _T_ , the _O_ (1 _/T_ ) dominates, so that the error is _O_ ( _ε_ ). Recall that the sample complexity is _O_<sup>�</sup> �ln _T ·_ ln<sup><u>ln</u></sup> _δ_<sup>_<u>T</u>_</sup> �, which to the higher order multiplicative term is _O_<sup>�</sup> (log 1 _/ε_ ). 

21 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

### **5.4. Comparison to Other Non-convex Optimization Methods** 

Our sample complexity bound decouples the problem parameters such as dimension _n_ from the precision _ε_ , yielding a _O_<sup>˜</sup> (log 1 _/ε_ ) sample complexity, with constants depending on problem parameters. We compare this guarantee with extant methods for non-convex optimization. 

**1. Grid Search (Lipschitz Optimization):** Standard spatial discretization algorithms require _O_ ((1 _/ε_ )<sup>_n_</sup> ) function evaluations, so the precision parameter _ε_ gets exponentially modified. 

**2. Local MCMC and Simulated Annealing:** While local Markov chains scale polynomially in dimension on convex bodies, they can take exponential time in non-convex landscapes. The Holley-Stroock perturbation lemma (Holley and Stroock, 1987) implies escaping a local minimum of depth ∆ _E_ at inverse temperature _τ_ requires mixing time _O_ (exp( _τ_ ∆ _E_ )), and Hajek’s theorem (Hajek, 1988) implies guaranteeing convergence in local MCMC simulated annealing requires a logarithmic cooling schedule _τt_ = _O_ (ln _t_ ). These results mean that in the worst case, classical simulated annealing may require _O_ (exp(1 _/ε_ )) steps, so again, the precision parameter is exponentially modified. 

To mitigate these slow mixing times, classical MCMC and simulated annealing often employ variance-inflated distributions, either as heavier-tailed proposals to guarantee ergodicity (Mengersen and Tweedie, 1996) or as “warm starts” to bound the density ratio between temperature steps (Lovász and Vempala, 2006). However, classical methods utilize variance inflation to aid _local_ random walks, which can take exponentially many samples for non-convex landscapes. In contrast, ALDRIFT adapts the variance-inflation principle to bound the mass coverage of a _generative proxy_ . The proxy dynamically absorbs empirical estimation errors independent of the annealing temperature, allowing the algorithm to achieve logarithmic sample complexity. 

**3. Deterministic Optimistic Optimization (DOO):** Among finite-sample methods, the closest comparators are optimistic partitioning methods such as DOO (Bubeck et al., 2011), SOO (Munos, 2011) and their stochastic/noisy variants (e.g. HOO/StoSOO (Valko et al., 2013) and POO Grill et al. (2015)). In contrast, classical Lipschitz branch-and-bound methods Piyavskii (1972); Shubert (1972) only convergence in different regimes. When the objective is bounded by a quadratic envelope, spatial-partitioning algorithms (Munos, 2011; Bubeck et al., 2011) achieve _O_<sup>�</sup> (log(1 _/ε_ )) sample complexity. These methods hierarchically search the space via optimistic estimates of the objective within grid partitions. ALDRIFT achieves this same characteristic rate, but under different trade-offs. Unlike these methods, ALDRIFT requires prior estimates of both the upper and lower bounds on the curvature parameters ( _µd, Ld_ ), and its sample complexity scales with the full ambient dimension _n_ , whereas space-partitioning bounds scale with the near-optimality dimension, which could be smaller. Furthermore, extensions like SOO (Munos, 2011) only require the existence of an upper bounding quadratic without needing to know its parameters, a setting ALDRIFT does not handle. Addressing these limitations in ALDRIFT is an exciting direction for future work. 

On the other hand, space-partitioning operations are harder to define for discrete, combinatorial, or semantic generative spaces (e.g., sequences generated by LLMs). The ALDRIFT algorithm matches the sample complexity of space partitioning methods for quadratic-bounded functions, while generalizing as an algorithmic framework to other generative priors and discrete optimization objectives whenever Assumption 2 holds. 

22 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

## **6. Empirical Illustration of ALDRIFT versus TOPIFT** 

Although our contributions are primarily theoretical, we present a focused empirical demonstration to validate the necessity of an optimistic, variance-inflated proposal distribution combined with sample correction. We compare ALDRIFT against TOPIFT, a baseline that relies on empirical variance without distribution correction and consequently suffers from premature convergence to local optima. While specialized heuristics exist to navigate specific non-convex landscapes, our objective here is not to achieve state-of-the-art empirical performance. Rather, our goal is to cleanly isolate and verify how the core theoretical insights of our framework hold up under strict sample budgets. 





Figure 1: Optimization error trajectories ( _||µ − x_<sup>_∗_</sup> _||_ ) versus iteration for ALDRIFT and TOPIFT. **(Left)** Parameters: _µd_ = 0 _._ 5 _, A_ = 2 _._ 0 _, ω_ = 3 _._ 0 _, x_ 0 = **6** _, µ_ 0 = 0 _._ 1. **(Center)** Parameters: _µd_ = 1 _._ 0 _, A_ = 0 _._ 5 _, ω_ = 4 _._ 0 _, x_ 0 = **1** _._ **35** _, µ_ 0 = 2 _._ 0. **(Right)** Pr[Accept] of a sample versus the temperature _τ_ in ALDRIFT. 

**Objective Landscape.** We study the non-convex optimization setting from Section 5 and define a _n_ = 10 dimensional objective _d_ ( _·_ ) characterized by a global quadratic envelope and high-frequency local minima. For _x ∈_ R<sup>10</sup> , let _d_ ( _x_ ) =<sup>_<u>µ</u>_</sup> 2<sup>_<u>d</u>∥x∥_2 +</sup><sup>_A_</sup><sup><u>�</u></sup> _i_<sup>10</sup> =1<sup>(1</sup><sup>_−_cos(</sup><sup>_ωxi_)).The global minimum is</sup> located at _x_<sup>_∗_</sup> = **0** . We initialize the prior _L_ 0 = _N_ ( _x_ 0 _, µ_<sup><u>2</u></sup> 0<sup>_In_) with</sup><sup>_x_0far enough that the optimizer</sup> must traverse multiple local optima to succeed. Following the setting in Section 5 assume _µd_ is known to ALDRIFT as a lower bound on curvature at the optimum solution. **Algorithms.** We evaluate both ALDRIFT and TOPIFT using a shared sample budget. • **ALDRIFT (Variance Inflated):** We employ the geometric annealing schedule (as described in Section 5), updating the temperature as _τk_ +1 = (1 + 1 _/n_ ) _τk_ from an initial _τ_ 0 = 0 _._ 1 to _T_ = 20. At each step, we use Metropolis-Hastings to draw _m_ = 200 samples, with a chain length of _M_ = 50. Crucially, the model is updated using the inflated variance _Lτ_ ( _x_ ) = _N_ (ˆ _ωτ , µ_<sup><u>2</u></sup> _τ_<sup>_In_), where</sup><sup>_µτ_=</sup><sup>_µ_0 +</sup><sup>_τµd_and</sup><sup>_ω_ˆ</sup><sup>_τ_is the sample mean.</sup> 

- **TOPIFT (Empirical Variance):** The heuristic samples _m·M_ times directly from the current Gaussian model, scores them based on _d_ ( _x_ ), selects the top _m_ samples, and fits the next Gaussian model using their empirical mean and empirical covariance. 

**Results.** Figure 1 (left and center figures) plots the error of the sample mean of the model _Lτ_ as a function of iteration number for two different settings of the parameters, averaged over 10 runs for each algorithm. TOPIFT falls into a sub-optimal local minimum because the elite samples are concentrated in a single valley and the empirical variance shrinks to near-zero. Conversely, ALDRIFT 

23 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

successfully converges close to the global optimum by using an inflated proposal distribution and correcting for it every iteration, empirically validating Theorem 3. 

Observe that ALDRIFT converges _close_ to the global optimum, but does not reach it exactly. This occurs because we operate in a highly constrained sampling regime where _M_ is much smaller than the theoretical requirement for convergence. Consequently, as the temperature increases and the target distribution sharpens, the probability of an accepting M-H transition approaches zero (see Fig. 1, Right). (A similar stalling effect is observed in our LLM experiments in Section 9.) Thus, the primary practical advantage of ALDRIFT lies in its ability to rapidly isolate the global basin of attraction using a limited sample budget. Once there, standard local optimization methods can be applied to precisely locate the exact optimum. This contrasts with TOPIFT, which frequently becomes trapped in suboptimal local minima under comparable sample constraints. Conversely, in the asymptotic regime where sample size is unconstrained, naive exploration strategies such as grid search or TOPIFT become competitive by brute-forcing the objective landscape, analogous to the asymptotic convergence guarantees of the Cross-Entropy method and MRAS Rubinstein (1999); Hu et al. (2007). 

## **7. Theoretical Evidence for Coarse Learnability** 

Complementing the sample complexity proof in Section 5, we now present theoretical evidence to support the coarse learnability assumption (Assumption 2) for simple generative models. First, to demonstrate robustness in the _agnostic_ setting, we prove that a structurally misspecified learner (a single Gaussian) naturally satisfies the coverage condition when approximating a multimodal target (Section 7.1). Second, to validate consistency with classical MBO theory, we show that standard MLE in the _realizable_ setting of MRAS (i.e., exponential families) satisfies the assumption with high probability (Section 7.2). Finally, we demonstrate that coarse learnability extends to a simple Kernel Density Estimation (KDE) task, provided the kernel is deliberately “over-smoothed” to act as a robust coverage envelope (Section 7.3). 

### **7.1. Gaussian Mixtures and Robustness to Mis-specification** 

Assumption 2 particularly relevant in the agnostic or misspecified setting, where the learner cannot model the complex shape of the target but can learn to cover its support. Indeed, when a lower-capacity model (like a restricted neural network or a single Gaussian) approximates a complex, multimodal target, the MLE objective forces the learner to “spread out” and envelope the target’s support rather than collapsing to a single mode (Minka, 2005). In our setting, the generative model learns to act as this relaxed envelope. 

We illustrate this with a Gaussian mixture model target and a single Gaussian learner. Let the target _p_ ( _x_ ) be a mixture of _k_ unit-variance Gaussians: 



Let the learner _L_ be restricted to the family of single Gaussians _N_ ( _θ, σ_<sup>2</sup> ). This is a mis-specified setting where _d_ TV( _p, L_ ) cannot be made arbitrarily small. However, we show that MLE naturally satisfies Assumption 2. 

24 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

**Theorem 12** _Let the target p_ ( _x_ ) = _k_<sup><u>1</u></sup> � _ki_ =1<sup>_N_(</sup><sup>_µi,_1)</sup><sup>_beamixtureofkunit-varianceGaussians_</sup> _with means µi ∈_ [ _−_<sup><u>∆</u></sup> 2<sup>_,_</sup><sup><u>∆</u></sup> 2<sup>]</sup><sup>_, where_∆</sup><sup>_≥_2</sup><sup>_.Assume the modes are sufficiently separated such that the_</sup> _population variance satisfies σ_<sup>_∗_2</sup> _≥_ 2 _. Let L_ MLE _be the single Gaussian model N_ (ˆ _µ,_ ˆ _σ_<sup>2</sup> ) _learned via MLE on m i.i.d. samples from p._ 

_If m_ = Ω(∆<sup>4</sup> ln(1 _/δ_ )) _, then with probability at least_ 1 _− δ, the learned model satisfies the global coverage condition:_ 



_Thus, for a fixed number of modes k, the model family satisfies Assumption 2 with m scaling polynomially in K_ = _O_ (∆) _and_ ln(1 _/δ_ ) _._ 

**Proof** Let _µ_<sup>_∗_</sup> and _σ_<sup>_∗_2</sup> denote the true mean and variance of the target mixture _p_ . The mean of the mixture is _µ_<sup>_∗_</sup> = _k_<sup><u>1</u></sup> � _µi_ . The variance of the mixture is given by the law of total variance: 



From this identity, we observe that the squared deviation of any single component mean is bounded by the total variance scaled by _k_ : 



By the premise, _σ_<sup>_∗_2</sup> _≥_ 2. Since the means are bounded in width ∆, we also have _σ_<sup>_∗_2</sup> _≤_ 1 + ∆<sup>2</sup> . 

The MLE parameters are the sample mean ˆ _µ_ and sample variance ˆ _σ_<sup>2</sup> . The target distribution _p_ is a mixture of Gaussians with bounded parameter support. Since the component means are bounded by ∆ _/_ 2 and the component variances are fixed at 1, the random variable _X ∼ p_ is sub-Gaussian with norm _∥X∥ψ_ 2 = _O_ (∆). First, by Hoeffding’s inequality (Vershynin, 2018), for any _t >_ 0 (where _c_ is a constant). 



Next, the variable _X_<sup>2</sup> is sub-exponential with _∥X_<sup>2</sup> _∥ψ_ 1 = _O_ (∆<sup>2</sup> ), so by Bernstein’s inequality (Vershynin, 2018): 



We choose a sampling error tolerance _η_ as a sufficiently small constant. To ensure _|µ_ ˆ _− µ_<sup>_∗_</sup> _| ≤ η_ and _|σ_ ˆ<sup>2</sup> _− σ_<sup>_∗_2</sup> _| ≤ η_ with probability 1 _− δ_ , we need _m_ = Ω(∆<sup>4</sup> ln(1 _/δ_ )). Conditioned on this high-probability event, and using _σ_<sup>_∗_2</sup> _≥_ 2, we have _σ_ ˆ<sup>2</sup> _>_ 1. 

The coverage ratio is _r_ ( _x_ ) = _L_<sup>_<u>p</u>_</sup><sup><u>(</u></sup> (<sup>_x_</sup> _x_<sup><u>)</u></sup> )<sup>=</sup> _k_<sup><u>1</u></sup> � _ki_ =1 _NN_ (( _xx_ ;ˆ; _µ,µiσ_ ˆ _<u>,</u>_ 1<sup>2</sup> <u>))</u><sup>.It suffices to bound an arbitrary term</sup> _Ti_ ( _x_ ) =<sup>_N_</sup><sup><u>(</u></sup><sup>_x_</sup><sup><u>;</u></sup><sup>_<u>µi,</u>_1)</sup> _N_ ( _x_ ;ˆ _µ,σ_ ˆ<sup>2</sup> )<sup>:</sup> 



25 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

Let _Ei_ ( _x_ ) be the exponent. Differentiating with respect to _x_ : 



Setting _Ei_<sup>_′_(</sup><sup>_x_) = 0 yields the unique maximum at:</sup> 



Substituting this back into _Ei_ ( _x_ ), the exponent at the maximum simplifies to: 



We now apply the finite sample bounds derived above. First, consider the numerator ( _µi − µ_ ˆ)<sup>2</sup> . Since _|µ_ ˆ _− µ_<sup>_∗_</sup> _| ≤ η_ , we have 



Using the population variance bound from Eq. (5), let _V_ = _σ_<sup>_∗_2</sup> _−_ 1. Then ( _µi − µ_<sup>_∗_</sup> )<sup>2</sup> _≤ kV_ , which implies _|µi − µ_<sup>_∗_</sup> _| ≤ √kV_ . Thus: 



Next, consider the denominator 2(ˆ _σ_<sup>2</sup> _−_ 1). Using _|σ_ ˆ<sup>2</sup> _− σ_<sup>_∗_2</sup> _| ≤ η_ : 



Since we assumed _σ_<sup>_∗_2</sup> _≥_ 2, we have _V ≥_ 1. Since _η ≤_ 0 _._ 5, we have _V − η ≥ V_ (1 _− η_ ) _≥_ 0 _._ 5 _V_ . For small enough constant _η_ , the exponent _Ei_ ( _x_<sup>_∗_</sup> ) is bounded by: 



Consequently, the maximum value of the component ratio is: 



Since _σ_ ˆ<sup>2</sup> _≤ σ_<sup>_∗_2</sup> + _η ≤_ 2 + ∆<sup>2</sup> , we have _σ_ ˆ _≤ O_ (∆). 

Summing over the _k_ components (each with weight 1 _/k_ ): 



We can now choose any _m ≥_ poly �ln<sup><u>1</u></sup> _δ_<sup>_,_∆</sup><sup>_, ek_�</sup> to satisfy Assumption 2. Note that the coverage condition holds globally. 

26 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

### **7.2. Exponential Families and Realizable Setting** 

We now present theoretical justification for coarse learnability for simple distributions. We consider the class of exponential families with a single parameter and show that under benign assumptions on the family, the MLE estimation problem is coarsely learnable. This result extends to some multi-parameter settings, and we present a sketch at the end omitting the details. Note that single-parameter exponential families capture most common distributions such as Gaussian, Exponential, Poisson, Binomial, etc. This result shows that coarse learnability is a natural property of standard statistical estimation in well-behaved settings. 

It is important to contextualize the result below within the model reference adaptive search (MRAS) literature. As discussed in Appendix A.3, standard MRAS utilizes natural exponential families for the parametric model (Hu et al., 2007). While true target distributions are generally complex, analyzing the idealized “realizable” setting, where the target falls within the model family, serves as a theoretical baseline. The analysis below confirms that in this realizable setting, the finite-sample MLE inherently satisfies our coarse learnability assumption. This indicates that our statistical condition is well-grounded, holding for standard parametric families in an idealized realizable setting. Crucially, however, as discussed in Section 7.1, our framework extends guarantees beyond this idealized case to the more general agnostic setting where the target is complex and the model is misspecified, by utilizing the Metropolis–Hastings correction. 

**Single-Parameter Setting.** Let _p_ ( _x | η_ ) = _h_ ( _x_ ) _· e_<sup>_ηx−A_(</sup><sup>_η_)</sup> be a single-parameter exponential family and let _X_ denote a random variable following this distribution. Let _µ_ ( _η_ ) = E _X∼p_ ( _x|η_ )[ _X_ ] = _A_<sup>_′_</sup> ( _η_ ). We suppose the exponential family satisfies the following simple assumption. 

**Assumption 3 (Regularity)** _We assume the density p_ ( _x | η_ ) _is sub-exponential._<sup>4</sup> _Further, the true parameter η_ 0 _lies in a constant-sized closed interval_ Ω0 _such that for all η ∈_ Ω0 _, we have that A_ ( _η_ ) _is analytic and_ 0 _< v_ min _≤ A_<sup>_′′_</sup> ( _η_ ) _≤ v_ max _< ∞ for some positive constants v_ min _, v_ max _._ 

The above assumption holds for common distributions such as Gaussian, Bernoulli, Exponential, and Poisson under mild conditions on their parameters. These densities are clearly subexponential. Furthermore, we have the following: 

**Gaussian (with known variance).** We have _p_ ( _x | µ_ ) = _~~√~~_ 21 _πσ_<sup>2</sup><sup>_e−_(</sup><sup>_x−µ_)2</sup><sup>_/_(2</sup><sup>_σ_2).Therefore,</sup><sup>_η_=</sup> _µ/σ_<sup>2</sup> and _A_ ( _η_ ) = _η_<sup>2</sup> _σ_<sup>2</sup> _/_ 2, so that _A_<sup>_′′_</sup> ( _η_ ) = _σ_<sup>2</sup> , which is a constant. 

- **Bernoulli.** We have _p_ ( _x | µ_ ) = _µ_<sup>_x_</sup> (1 _− µ_ )<sup>1</sup><sup>_−x_</sup> for _x ∈{_ 0 _,_ 1 _}_ . We have _η_ = ln( _µ/_ (1 _− µ_ )), and _A_ ( _η_ ) = ln(1 + _e_<sup>_η_</sup> ) = _−_ ln(1 _− µ_ ). We have _A_<sup>_′′_</sup> ( _η_ ) = _e_<sup>_η_</sup> _/_ (1 + _e_<sup>_η_</sup> )<sup>2</sup> = _µ_ (1 _− µ_ ), which satisfies the above assumption when _µ ∈_ [ _δ,_ 1 _− δ_ ] for constant _δ >_ 0. 

- **Exponential.** We have _p_ ( _x | λ_ ) = _λe_<sup>_−λx_</sup> for _x ≥_ 0. Further, we have _η_ = _−λ_ and _A_ ( _η_ ) = _−_ ln( _−η_ ), so that _A_<sup>_′′_</sup> ( _η_ ) = 1 _/η_<sup>2</sup> , which satisfies the above assumption when _λ >_ 0 is a constant. 

- **Poisson.** We have _p_ ( _x | λ_ ) = _e_<sup>_−λ_</sup> _λ_<sup>_x_</sup> _/x_ ! for _x_ = 0 _,_ 1 _,_ 2 _, . . ._ . We have _η_ = ln _λ_ , _A_ ( _η_ ) = _e_<sup>_η_</sup> , and _A_<sup>_′′_</sup> ( _η_ ) = _e_<sup>_η_</sup> = _λ_ , which satisfies the assumption when _λ >_ 0 is a constant. 

> 4. A sub-exponential random variable satisfies Pr[ _|X| ≥ K_ ] _≤_ 2 _e_<sup>_−C·K_</sup> for all _K ≥_ 0 and some constant _C >_ 0. 

27 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

The derivation of coarse learnability under Assumption 3 uses standard properties of subexponential distributions; see, e.g., (Vershynin, 2018) for details. Since we assumed the exponential family is sub-exponential, this means there exist positive constants _C_ 1 _, C_ 2 _>_ 0 such that for _X ∼ p_ ( _x | η_ 0): 



This also means (Vershynin, 2018) that there are constants _ν_<sup>2</sup> _, α_ such that for random variable _X_ following _p_ ( _x | η_ ), we have: 



Let _Z_ = _X − µ_ ( _η_ ), so that E[ _Z_ ] = 0. Clearly, _Z_ is also sub-exponential, and satisfies the above equation for some _ν_<sup>2</sup> _, α_ . Suppose we draw _m_ samples from _p_ ( _x | η_ ) and let _X_<sup>ˆ</sup> be their average: 



Choosing _λ_ = _νε_<sup>2</sup><sup>_<_</sup> _α_<sup><u>1</u>(assuming</sup><sup>_ε_=</sup><sup>_o_(1)), we have</sup> 



Choosing _ε_ = _m_<sup>_−_1</sup><sup>_/_3</sup> , this implies: 



We are now ready to show the following theorem, which we show implies Assumption 2. 

**Theorem 13** _Suppose the exponential family satisfies Assumption 3. Let η_ ˆ _m be the MLE of η_ 0 _based on m samples, satisfying A_<sup>_′_</sup> (ˆ _ηm_ ) = _X_ ¯ _m, where X_ ¯ _m is the average of m samples. Let L_ ( _x_ ) _≡ p_ ( _x | η_ ˆ _m_ ) _. For any small constant γ >_ 0 _, define_ 



_Then, for any m ≥_ poly � _<u>vv</u>_ <u>maxmin</u><sup>_,_</sup> _ν_<sup><u>1</u></sup> � _and a sufficiently small constant γ >_ 0 _, with probability_ 1 _−_ 2 _e_<sup>_−mγ_</sup> _, the parameter η_ ˆ _m satisfies_ Pr[ _X ∈/ Wm_ ] _≤ e_<sup>_−mγ_</sup> _._ 

**Proof** Let ∆ _η_ = _η_ ˆ _m − η_ 0. The log-density ratio is 

_R_ ( _x_ ) = ln _p_ ( _x | η_ 0) _−_ ln _p_ ( _x | η_ ˆ _m_ ) = ( _η_ 0 _− η_ ˆ _m_ ) _· x_ + ( _A_ (ˆ _ηm_ ) _− A_ ( _η_ 0)) _._ 

Using a Taylor expansion for _A_ (ˆ _ηm_ ) = _A_ ( _η_ 0 + ∆ _η_ ) around _η_ 0 up to the second term, for some _ξ_ between _η_ 0 and _η_ ˆ _m_ , we have 



28 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

Substituting this into _R_ ( _x_ ): 



Let _µ_ ( _η_ 0) = _A_<sup>_′_</sup> ( _η_ 0) be the true mean. By Eq. (7), the event _E_ param := _{_ �� _X_ ¯ _m − µ_ ( _η_ 0)�� _≤ m_<sup>_−_1</sup><sup>_/_3</sup> _}_ occurs with probability at least 1 _−_ exp( _−m_<sup>1</sup><sup>_/_3</sup> _/ν_<sup>2</sup> ). The MLE satisfies _A_<sup>_′_</sup> (ˆ _ηm_ ) = _X_<sup>¯</sup> _m_ = _µ_ (ˆ _ηm_ ). On _E_ param, we therefore have _|A_<sup>_′_</sup> (ˆ _ηm_ ) _− A_<sup>_′_</sup> ( _η_ 0) _| ≤ m_<sup>_−_1</sup><sup>_/_3</sup> . By the Mean Value Theorem, _A_<sup>_′_</sup> (ˆ _ηm_ ) _− A_<sup>_′_</sup> ( _η_ 0) = _A_<sup>_′′_</sup> ( _η_<sup>_∗_</sup> )(ˆ _ηm − η_ 0) for some _η_<sup>_∗_</sup> between _η_ 0 and ˆ _ηm_ . By Assumption 3, _A_<sup>_′′_</sup> ( _η_<sup>_∗_</sup> ) _≥ v_ min _>_ 0. Thus, on _E_ param, we have 



This implies (∆ _η_ )<sup>2</sup> _≤_<sup>_<u>m</u>_</sup> _v_<sup>_−_</sup> min<sup>22</sup><sup>_/_3.Also, on</sup><sup>_E_param,</sup><sup>_A′′_(</sup><sup>_ξ_)</sup><sup>_≤v_maxby Assumption 3.This implies the</sup> first term ∆ _η_ ( _A_<sup>_′_</sup> ( _η_ 0) _− x_ ) dominates in the equation for _R_ ( _x_ ) when _m ≥_ poly � _<u>vv</u>_ <u>maxmin</u> �. Thus, for _|R_ ( _x_ ) _| ≤ m_<sup>_−_1</sup><sup>_/_3+</sup><sup>_γ_</sup> , we require: 



Since _|_ ∆ _η| ≤_<sup>_<u>m</u>_</sup> _v_<sup>_−_</sup> min<sup>1</sup><sup>_/_3, this requires</sup><sup>_|A′_(</sup><sup>_η_0)</sup><sup>_−x| ≤_</sup> 2<sup><u>1</u></sup><sup>_v_min</sup><sup>_mγ_:=</sup><sup>_Km_.The set</sup><sup>_W_is then defined by</sup> _x_ such that _|x − µ_ ( _η_ 0) _| ≤ Km_ . By Eq. (6), we have Pr[ _x ∈/ W_ ] = _O_ � _e_<sup>_−O_(</sup><sup>_Km_)�</sup> . Choosing _γ >_ 0 an appropriately small constant, this completes the proof. Note that the failure probabilities in the above theorem are monotonically decreasing in _m_ . Therefore, if we are given _K >_ 1 _, ε >_ 0 _, δ >_ 0 as in Assumption 2, then we can simply choose a large enough _m ≥_ poly � _<u>vv</u>_ <u>maxmin</u><sup>_,_</sup> _ν_<sup><u>1</u></sup><sup>_,_ln</sup> _εδ_<sup><u>1</u></sup> � that ensures _e_<sup>_−mβ_</sup> _≤_ min ( _δ, ε_ ). Further, note that _m_<sup>_−_1</sup><sup>_/_3+</sup><sup>_γ_</sup> _<_ ln _K_ . This ensures that with probability 1 _− δ_ , we have Pr [ _p_ ( _x|η_ 0) _≥ K · p_ ( _x|η_ ˆ _m_ )] _≤ ε_ , hence satisfying Assumption 2. 

**Multi-Parameter Setting.** Let _p_ ( **x** _|_ **_η_** ) = _h_ ( **x** ) exp( **_η_**<sup>_T_</sup> **x** _− A_ ( **_η_** )) be a _k_ -parameter exponential family, where **_η_** _∈ℜ_<sup>_k_</sup> and **x** _∈ℜ_<sup>_k_</sup> , and _k_ being a constant. This for instance, captures multidimensional Gaussian distributions with a known covariance matrix, or multinomial distributions. Assuming the resulting density is sub-exponential in the _ℓ_ 2-norm, it can be shown that such a distribution satisfies Eq. (6) and Eq. (7) with the absolute value replaced by the _ℓ_ 2-norm, and the constants depending on _k_ . In particular, the _ℓ_ 2-norm of the deviation from the mean is a sub-exponential random variable. By re-working the same proof as that of Theorem 13, this implies an analog of Theorem 13 to the multi-dimensional setting, under suitable regularity assumptions on _A_ ( **_η_** ). The details are easy to fill in, and omitted. 

### **7.3. Over-smoothed Non-Parametric Estimation** 

The previous sections demonstrated that coarse learnability arises naturally in parametric settings due to the mass-covering properties of Maximum Likelihood Estimation. We now show that this principle extends to a simple non-parametric Kernel Density Estimation (KDE) task, provided the estimator is deliberately “over-smoothed.” 

29 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

In classical density estimation, the bandwidth _h_ of a kernel is typically shrunk as the sample size _m →∞_ to recover the exact target density. However, in our optimization framework, a shrinking bandwidth creates light tails that exponentially under-cover the target’s support, violating Assumption 2. Conversely, if we fix a kernel whose bandwidth dominates the target’s tail decay, the KDE forms a robust coverage envelope. We formalize this in _d_ -dimensions. 

**Theorem 14** _Let the target distribution p_ ( _x_ ) = _N_ (0 _, σ_<sup>2</sup> _Id_ ) _be a d-dimensional isotropic Gaussian. Let LKDE_ ( _x_ ) = _m_ <u>1</u> � _mi_ =1<sup>_Kh_(</sup><sup>_x−Xi_)</sup><sup>_bethedensitylearnedviaKDEusingaGaussiankernel_</sup> _Kh_ ( _z_ ) = (2 _πh_<sup>2</sup> )<sup>_−d/_2</sup> exp( _−∥z∥_<sup>2</sup> _/_ 2 _h_<sup>2</sup> ) _on m i.i.d. samples X_ 1 _, . . . , Xm from p._ 

_Assume we set the bandwidth to match_<sup>5</sup> _the target’s tail decay, h_ = _σ. There exists a universal constant C >_ 0 _such that if the sample size satisfies m ≥ C_ ( _d_ + ln(1 _/δ_ )) _, then with probability at least_ 1 _− δ over the samples, the learned model globally satisfies the coarse learnability condition:_ 



_This implies m_ = _O_ �ln<sup>_<u>K</u>_</sup> _δ_ � _, showing Assumption 2._ 

**Proof** We first show that for any query point _x ∈_ R<sup>_d_</sup> , a constant fraction of the empirical samples simultaneously resides near the origin and directionally points toward _x_ . 

Let _B_ = _{y ∈_ R<sup>_d_</sup> : _∥y∥_<sup>2</sup> _≤_ 2 _σ_<sup>2</sup> _d}_ be the closed ball of radius _σ√_ 2 _d_ centered at the origin. For _X ∼N_ (0 _, σ_<sup>2</sup> _Id_ ), the expected squared norm is E[ _∥X∥_<sup>2</sup> ] = _σ_<sup>2</sup> _d_ . By Markov’s inequality, the probability that a sample falls outside this ball is bounded by: 



Thus, the true probability mass of the ball is Pr( _X ∈B_ ) _≥_ 1 _/_ 2. 

For any query point _x ∈_ R<sup>_d_</sup> , define the halfspace pointing toward _x_ as _Hx_ = _{y ∈_ R<sup>_d_</sup> : _⟨x, y⟩≥_ 0 _}_ . Because the Gaussian distribution is spherically symmetric and centered at the origin, exactly half of the mass of _B_ lies in _Hx_ . Therefore, the true probability that a random sample falls into their intersection is: 



We require the empirical fraction of samples in _B ∩ Hx_ to tightly concentrate around its true expectation uniformly over all possible directions _x ∈_ R<sup>_d_</sup> . The set of such halfspaces _{Hx_ : _x ∈_ R<sup>_d_</sup> _}_ has VC dimension of _d_ . Intersecting this class with a fixed set _B_ does not increase the VC dimension. By uniform convergence, there exists a universal constant _c >_ 0 such that with probability at least 1 _− δ_ : 



We choose the sample size _m_ sufficiently large such that this uniform error is bounded by 1 _/_ 8. Specifically, this requires _m ≥ C_ ( _d_ + ln(1 _/δ_ )) for _C_ = 64 _c_<sup>2</sup> . 

5. The proof easily extends to _h_ = _c · σ_ for constant _c ≥_ 1. 

30 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

Under this condition, with probability 1 _− δ_ , the empirical fraction of samples falling in _B ∩ Hx_ is at least _px −_ 1 _/_ 8 _≥_ 1 _/_ 4 _−_ 1 _/_ 8 = 1 _/_ 8 for all _x_ simultaneously. Let _Sx_ = _{Xi_ : _Xi ∈B ∩ Hx}_ be this subset of samples for a given _x_ . We are guaranteed that _|Sx| ≥ m/_ 8 for every _x ∈_ R<sup>_d_</sup> . 

Conditioned on this uniform convergence event, we evaluate the ratio _r_ ( _x_ ) = _p_ ( _x_ ) _/L_ KDE( _x_ ) for an arbitrary _x ∈_ R<sup>_d_</sup> . We lower bound the KDE sum by dropping all kernel components except those corresponding to the samples in _Sx_ : 



For every _Xi ∈ Sx_ , we know two facts by definition of the set: _∥Xi∥_<sup>2</sup> _≤_ 2 _σ_<sup>2</sup> _d_ and _⟨x, Xi⟩≥_ 0. Expanding the squared distance yields: 



Substituting this upper bound on the distance into each kernel exponent in the sum gives: 



Because _|Sx| ≥ m/_ 8 for all _x_ , we have 



This completes the proof. 

Our proof easily extends to the setting where _h_ = _c · σ_ for constant _c ≥_ 1 and yields _K_ = _O_ (( _ce_ )<sup>_d_</sup> ). Further, the same proof idea generalizes to centrally symmetric sub-Gaussian distributions with similar bounds. 

## **8. Motivating Application: Algorithm-LLM Interaction at Inference-time** 

One of our motivations for studying MBO with expressive, black-box generative priors comes from algorithm-LLM interaction, specifically via inference-time alignment. Increasingly, real-world combinatorial optimization requires balancing strict global constraints (e.g., graph connectivity, efficiency) with informal, context-dependent local specifications (e.g., scenic preferences, stylistic coherence). While classical algorithms efficiently solve for global feasibility, they are brittle when handling qualitative or ambiguous requirements (Wang et al., 2023). Similarly, while modern LLMs excel at interpreting open-ended requirements Radford et al. (2018); Brown et al. (2020), they consistently struggle to enforce global combinatorial properties. We illustrate this limitation empirically using a cycle detection task. As shown in Figure 2, when asked to find a length- _k_ cycle in a graph containing a planted cycle, models such as GPT-4, Claude 3.5 Sonnet, and Claude 3.7 Sonnet show rapidly diminishing success rates as the cycle length _k_ increases. This shows that although models 

31 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 



Figure 2: Success rate of the models in finding a length _k_ -cycle in a graph as a function of _k_ . For each _k_ , the graph is constructed by starting with a cycle of length _k_ and randomly adding _⌈k/_ 2 _⌉_ other edges. For each cycle length _k_ , we generate 50 random instances and compute the success rate, i.e., the fraction of times the model returns a length- _k_ cycle. See Appendix B for the exact prompt used. 

continue to improve rapidly (Gemini Team, 2024; OpenAI, 2024; DeepSeek-AI et al., 2025), their capacity for exact combinatorial search remains bounded by a “short-chain” reasoning frontier. 

While this combinatorial reasoning capability can occasionally be improved by fine-tuning a model for a specific global objective (Sanford et al., 2024; Merrill and Sabharwal, 2024), such a tuned model would lose its interpretive flexibility when presented with informal, context-dependent requirements at test time. This trade-off between interpretive flexibility and global optimality arises broadly in domains like robot navigation (Tellex et al., 2011), molecular design, and automated scheduling (Jobson and Li, 2024). 

Therefore, problems requiring both interpretive flexibility and enforcement of global constraints exceed the reach of either pure LLMs or pure classical algorithms. For example, in generating a scenic route between two locations, an LLM may expertly evaluate individual route segments for scenic value based on natural language criteria, but it struggles to ensure those segments connect to form a valid, continuous path (Mei et al., 2016). Conversely, a combinatorial algorithm easily ensures path connectivity but cannot interpret the qualitative concept of “scenic-ness.” Similar complementary trade-offs exist in conference planning (Jobson and Li, 2024), where an LLM can semantically analyze abstracts to cluster sessions, but a classical algorithm is required to schedule them into a conflict-free timetable. This interaction is therefore best studied as model-based optimization with expressive black-box generative priors, providing a high-level motivation for the current work. 

Within this space, our motivation for MBO comes from inference-time alignment, where a fixed base model is adapted at test time using a reward signal or cost function. Indeed, TOPIFT and ALDRIFT are analogous to a test-time training step in LLMs (Sun et al., 2020), in that model fitting (that is, fine-tuning) is performed separately for each problem instance. See also (Huang et al., 2025; Chen et al., 2025; Madaan et al., 2023) for other empirical inference time alignment procedures. Our framework provides complementary theoretical bounds (under the coarse learnability assumption) to this line of work. 

32 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

## **9. Empirical Plausibility of Assumption 2** 

We now present some empirical evidence to support coarse learnability. The rigorous theoretical guarantees established in Section 4 and Section 5 rely on analytic generative models. Given the difficulty with showing corresponding results for algorithm-LLM interaction, we treat the coarse learnability condition (Assumption 2) in this section as an empirical heuristic rather than a provable guarantee. The primary contribution of this work is theoretical, and the goal of these experiments is merely to qualitatively study the empirical dynamics of these models. Specifically, we aim to test whether iterative fitting on a very small number of low-cost samples can heuristically shift an LLM’s distribution in the spirit of coarse learnability, namely, by demonstrating broader coverage over lower-cost regions. 

We use a primitive model, GPT-2, since it will demonstrate that our results are not a byproduct of the complex reasoning capabilities of frontier models, and applies to simple models as well. We also use the heuristic algorithm TOPIFT (Algorithm 1), which does not require estimating the LLM probabilities _L_ ( _s_ ) (Assumption 1) that is required for implementing ALDRIFT. This algorithm has the advantage of being simpler and implementable with frontier models where estimating probabilities directly is harder. We therefore present results for this heuristic, noting that the results for ALDRIFT are comparable and omitted for brevity. Accordingly, these experiments should be interpreted as qualitative evidence for the learnability intuition underlying Assumption 2 for LLMs rather than as an evaluation of ALDRIFT versus TOPIFT. 

### **9.1. Line Scheduling** 

We focus on a simplified line scheduling problem here, and also present results for the low degree spanning tree problem in Section 9.2. In the line scheduling problem, there are _K_ stations on a line labeled _{_ 1 _, . . . , K}_ . For 1 _≤ i < K_ , the travel time between station _i_ and _i_ + 1 is _ti_ . Each station _i_ has opening time _oi_ . The user specifies the intervals [ _ℓi, ui_ ] for 1 _≤ i ≤ K_ that capture the lower bound and the upper bound on how long they wish to spend at each station. The goal is to find a visit duration _vi_ for each _i ∈{_ 1 _, . . . , K}_ that specifies how much time the user should spend at each station; let **_v_** be the vector of these durations. If the user reaches a station before time _oi_ , then they need to wait there until time _oi_ . We constrain all numbers, including those generated by the LLM, to be integers. 

We split the problem constraints between a combinatorial algorithm that provides zeroth-order feedback on the objective _d_ ( _·_ ) and the LLM as follows. 

- **Algorithm’s Constraints.** Given a solution **_v_** , for _i ≥_ 2, let _ai_ be the arrival time at station _i_ , and _wi_ be the waiting time for the station to open; we assume _w_ 1 = _o_ 1 = 0. The total wait time is _d_ ( **_v_** ) =<sup>�</sup><sup>_K_</sup> _i_ =1<sup>_wi_, and this is the algorithm’s cost (or objective function).</sup> 

- **LLM’s Constraints.** The LLM’s constraints correspond to the visit time intervals [ _ℓi, ui_ ] for each point _i_ . Its cost is the total violation of the visit time computed as<sup>�</sup><sup>_K_</sup> _i_ =1<sup>_ηi_,where</sup><sup>_ηi_isthe</sup> distance of the visit time _vi_ from the interval [ _ℓi, ui_ ]. This quantity is 0 if _vi ∈_ [ _ℓi, ui_ ]. 

The LLM (GPT-2) is initially fine-tuned to satisfy only the local visit duration intervals, making it “oblivious” to the global waiting time constraint. This yields the model _L_ 0. We generate instances with _K_ = 10 and where each _ti, ℓi, ui_ is an integer in the range [1 _,_ 20] with the constraint _ℓi ≤ ui_ . For _i ≥_ 2, we set _oi_ = _oi−_ 1 + _ti−_ 1 + _ui−_ 1 _,_ so that there is a solution with wait time 0 if we set 

33 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

_vi ≥ ui_ for each _i_ . The only solution among these that also has a visit time violation 0 is the solution that sets _vi_ = _ui_ for each _i_ . 

In our experiment, we will consider the specific instance where the visit time bounds are set as _ℓi_ = 1 and _ui_ = 20, hence being vacuous, and all travel times are set to _ti_ = 10. For this instance, the optimal visit time vector is _⟨_ 20 _, . . . ,_ 20 _⟩_ , and this vector has wait time zero and visit time violation of 0. If the visit time at a station is _v <_ 20, then the solution has to wait 20 _− v_ steps before the next station opens. 





(a) (b) 

Figure 3: Box-plots of algorithm’s cost for the setting where the LLM’s visit time constraint is [1 _,_ 20]. In (a), for 20 runs of TOPIFT, the left two plots are the distribution of the algorithm’s cost for BEST-OF-LLM( _N_ ) baseline, while the right four plots are for TOPIFT after _r_ iterations. In (b), for one run of TOPIFT, for different values of iteration _r_ , the box-plot “ _r_ : _M_ ” is the distribution of the _m · M_ = 48 samples generated by the previous model, while “ _r_ : _T_ ” is the distribution of _m_ = 4 samples among these which have lowest algorithm’s cost (waiting time), and which are used for fine-tuning the new model. 

In Figure 3(a), we show the box plot, for 20 runs of the algorithm, of the algorithm’s cost (total wait time) for the BEST-OF-LLM baseline that draws _N_ samples from _L_ 0 and outputs the solution with minimum cost _d_ ( _·_ ). We plot this for _N_ = 1 and _N_ = 400 samples. Note that the median algorithm’s cost for BEST-OF-LLM for _N_ = 400 is at least 100. We observe that for any station, if _v_ is the visit time assigned to the station in a sample from _L_ 0, then assuming this is a uniform distribution on [1 _,_ 20], we would have E[ _v_ ] = 10 _._ 5, so that the expected wait time is (20 _−_ E[ _v_ ]) _·_ ( _K −_ 1) = 85 _._ 5. This roughly agrees with the baseline. Further note that Pr[ _v_ = 20] _≤_ 0 _._ 05. This is because the LLM is initially only aware of the bound _v ∈_ [0 _,_ 20], and hence, is likely to choose an integer visit time uniformly at random from this range. It is unaware of the global waiting time constraint. Assuming the dimensions behave independently, this means Pr[Wait time = 0] _≤_ 10<sup>_−_10</sup> , so that merely sampling from _L_ 0 is very unlikely to find a solution with optimal waiting time. 

We then compare this to TOPIFT (Algorithm 1) that fine-tunes _L_ iteratively using zeroth-order feedback about _d_ ( _·_ ). For TOPIFT, we set the parameters as _m_ = 4, _M_ = 12, and _Q_ = 8, so that the total number of samples used is comparable to _N_ = 400 used by the baseline. We consider 20 independent runs of the algorithm, and in Figure 3(a), we show the Box plot of the best waiting time 

34 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

obtained after _r_ iterations of the outer loop of TOPIFT. Though the BEST-OF-LLM baseline yields waiting time (objective _d_ ( _·_ )) of at least 100 even with _N_ = 400 samples, we note that TOPIFT improves on this even with _r_ = 4, generating the optimal visit-time vector almost always (wait time = 0) at _r_ = 8 iterations. 

In Figure 3(b), we show, for one run of the algorithm, the distribution of the _m · M_ = 48 samples generated by the model _Lr−_ 1 for 1 _≤ r ≤_ 8, and the distribution of the best _m_ = 4 samples (according to the algorithm’s cost) among these used for fine-tuning _Lr_ . Note that initially the fine-tuning samples move the model only slightly, while in later iterations the fine-tuned model produces solutions with substantially lower algorithmic cost than the fine-tuning data itself. Thus, the update is not merely memorizing the elite set, but shifting the model’s distribution further toward the low-cost region. This behavior is qualitatively analogous to Assumption 2: a learner trained on a small sample from a target distribution produces a proposal that covers that target directionally better than the raw sample alone would suggest.<sup>6</sup> While Figure 3(b) does not verify the density-ratio conclusion of Assumption 2, it provides empirical evidence for the kind of coarse, mass-covering extrapolation that the assumption posits. 

This phenomenon, where the model collapses to the optimal solution (Shumailov et al., 2024) demonstrates a remarkable ability of the LLM to extrapolate beyond the limited fine-tuning data. The iterative guidance from the zeroth-order feedback, even with a small sample size, enables the LLM to learn complex combinatorial constraints that it was initially unaware of. 

### **9.2. Low Degree Spanning Tree** 

In the low degree spanning tree problem, the input is a graph with _n_ = 16 vertices numbered 0 _,_ 1 _, . . . ,_ 15. We start by including the Hamiltonian path that includes all edges of the form ( _i, i_ +1) for _i ∈{_ 0 _,_ 1 _, . . . ,_ 14 _}_ . Next, for every pair of vertices, we add an edge between this pair with probability _p_ = 0 _._ 4, removing duplicates. Note that the expected degree of a vertex lies in [6 _,_ 8], and the graph has approximately 60 edges in expectation. 

The goal is to output a spanning tree minimizing the number of vertices with degree larger than two; in the ideal case, a Hamiltonian path. We split this problem between a combinatorial algorithm that captures the objective _d_ ( _·_ ) and LLM as follows: 

- **Algorithm’s Cost.** The algorithm simply wants to output a spanning tree. Given a solution _x_ as a list of edges, its cost _d_ ( _x_ ) is the number of connected components induced by _x_ minus 1, so that the optimal cost is 0, and the maximum possible cost is _n −_ 1 = 15. 

- **LLM’s Cost.** These correspond to the local node-wise degree constraints. We measure the cost of the LLM’s solution (set of edges) as the number of vertices whose degree is greater than 2. 

We fine-tune GPT-2 on forests with maximum degree two, yielding the base model _L_ 0. We then run the TOPIFT heuristic (Algorithm 1) with _m_ = 4, _M_ = 50, and _Q_ = 3. Note that the total number of samples is _N_ = _m · M · Q_ = 600. We compare to two baselines: In the BEST-OF-ALG baseline, we generate _N_ random spanning trees (all with cost _d_ ( _·_ ) = 0) and compute the probability assigned by _L_ 0 to each of them, choosing the best one. In the BEST-OF-LLM baseline, we generate _N_ solutions from _L_ 0 and score them according to the cost _d_ ( _·_ ), choosing the best one. 

> 6. We note that the same effect cannot be observed with only one round of fine-tuning — if we set _Q_ = 1, _m_ = 30, and _M_ = 12, and take the best waiting time of the samples from _L_ 0 and 40 samples from _L_ 1 (so that the total number of samples remains 400), we observe the waiting time is 81. This shows the advantage of the iterated framework. 

35 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 









<!-- Start of picture text -->
(a) Input graph. (b) BEST-OF-LLM,  N = 1. (c) BEST-OF-LLM,  N = 600.<br>(d) TOPIFT for  Q  = 3. (e) BEST-OF-ALG,  N = 1.<br><!-- End of picture text -->

Figure 4: Input graph and outputs of TOPIFT and the various baselines. Note that (b) is simply the output of the base model _L_ 0. The output of BEST-OF-ALG for _N_ = 600 and random spanning trees is comparable to (e), which means the model _L_ 0 assigns comparable probabilities to different random spanning trees. 

In Fig. 4, we illustrate the solutions found for a specific random test instance by the different baselines and TOPIFT. Note that samples from _L_ 0 satisfy the degree constraints, but are disconnected. BEST-OF-LLM for _N_ = 600 (Fig. 4(c)) improves connectivity but still finds a solution that is not only disconnected, but has degree violations. On the other hand, TOPIFT finds a Hamiltonian path<sup>7</sup> , hence achieving optimum cost for both the algorithm and LLM. Finally, note that random spanning trees (Fig. 4(e)), though connected, have many degree violations. (The latter is also essentially what BEST-OF-ALG for _N_ = 1 and _N_ = 600 generate.) This visually shows that TOPIFT is incorporating both the algorithm’s and the LLM’s constraints in a non-trivial fashion, indeed, finding the “optimum” solution on this instance. This showcases the power of the LLM in learning a complicated combinatorial constraint from a few samples, which aligns with coarse learnability. 

## **10. Conclusion** 

Our framework opens exciting avenues for future research. An ideal goal would be to prove a condition akin to coarse learnability for general LLMs, and a particularly compelling direction is to formally characterize the class of coarse learners and determine under what conditions modern LLMs fall into this category. For instance, which architectural features, training regimes, or fine-tuning strategies enable these models to satisfy the coarse learnability assumption? Addressing this question may require synthesizing insights from recent work on transformers and chain-ofthought reasoning through the lens of circuit complexity (Merrill and Sabharwal, 2024). Another 

> 7. This does not happen for all 15 test instances; however, TOPIFT finds one connected component in all instances. 

36 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

direction is to explore more powerful optimization oracles, such as those providing gradients of the log-probability, which could enable the use of Langevin MCMC in place of Metropolis–Hastings, potentially enhancing the efficiency and scalability of the framework. Finally, it would be interesting to extend Section 5 to work with weaker assumptions than quadratic bounding, and to extend ALDRIFT to remove Assumption 1. Collectively, these directions suggest a rich landscape for integrating statistical learning theory with combinatorial optimization, pointing toward a principled foundation for adaptive generative models. 

## **References** 

- Alekh Agarwal, Sham Kakade, Jason Lee, and Gaurav Mahajan. Optimality and approximation with policy gradient methods in Markov decision processes. In _COLT_ , 2020. 

- Christophe Andrieu, Arnaud Doucet, and Roman Holenstein. Particle markov chain monte carlo methods. _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ , 72 (3):269–342, 2010. doi:https://doi.org/10.1111/j.1467-9868.2009.00736.x. URL https://rss. onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9868.2009.00736.x. 

- S. Boucheron, G. Lugosi, and P. Massart. _Concentration Inequalities: A Nonasymptotic Theory of Independence_ . OUP Oxford, 2013. ISBN 9780199535255. URL https://books.google.com/ books?id=koNqWRluhP0C. 

- James A. Brofos, Marylou Gabrié, Marcus A. Brubaker, and Roy R. Lederman. Adaptation of the independent metropolis-hastings sampler with normalizing flow proposals. 2022. 

- Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In _NeurIPS_ , 2020. 

- Sébastien Bubeck, Rémi Munos, Gilles Stoltz, and Csaba Szepesvári. X-armed bandits. _JMLR_ , 12 (5), 2011. 

- O Cappé, A Guillin, J. M Marin, and C. P Robert. Population monte carlo. _Journal of Computational and Graphical Statistics_ , 13(4):907–929, 2004. doi:10.1198/106186004X12803. 

- Jiefeng Chen, Jie Ren, Xinyun Chen, Chengrun Yang, Ruoxi Sun, Jinsung Yoon, and Sercan Arık. SETS: leveraging self-verification and self-correction for improved test-time scaling. _TMLR_ , 2025. 

- DeepSeek-AI et al. Deepseek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning. _arXiv_ , 2501.12948, 2025. 

37 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

- Pierre Del Moral, Arnaud Doucet, and Ajay Jasra. Sequential monte carlo samplers. _Journal of the Royal Statistical Society Series B: Statistical Methodology_ , 68(3):411–436, 06 2006. ISSN 13697412. doi:10.1111/j.1467-9868.2006.00553.x. URL https://doi.org/10.1111/j.1467-9868. 2006.00553.x. 

- Abraham D. Flaxman, Adam Tauman Kalai, and H. Brendan McMahan. Online convex optimization in the bandit setting: gradient descent without a gradient. In _SODA_ , pages 385–394, 2005. 

- Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. _arXiv_ , 2403.05530, 2024. 

- Subhashis Ghosal and Aad van der Vaart. _Fundamentals of Nonparametric Bayesian Inference_ . Cambridge University Press, 2017. 

- Jean-Bastien Grill, Michal Valko, and Remi Munos. Black-box optimization of noisy functions with unknown smoothness. In _NIPS_ , 2015. 

- Bruce Hajek. Cooling schedules for optimal state in simulated annealing. _Math. OR_ , 13(2):311–329, 1988. 

- Matthew Hoffman, Pavel Sountsov, Joshua V. Dillon, Ian Langmore, Dustin Tran, and Srinivas Vasudevan. Neutra-lizing bad geometry in hamiltonian monte carlo using neural transport, 2019. URL https://arxiv.org/abs/1903.03704. 

- Richard A Holley and Daniel W Stroock. Logarithmic sobolev inequalities and stochastic ising models. _J. Stat. Phys._ , 46(5-6):1159–1194, 1987. 

- Jiaqiao Hu, Michael C Fu, and Steven I Marcus. A model reference adaptive search method for global optimization. _Operations Research_ , 55(3):549–568, 2007. 

- Audrey Huang, Adam Block, Qinghua Liu, Nan Jiang, Akshay Krishnamurthy, and Dylan J Foster. Is best-of-n the best of them? coverage, scaling, and optimality in inference-time alignment. In _ICML_ , 2025. 

- Mark Jerrum and Alistair Sinclair. _The Markov Chain Monte Carlo Method: An Approach to Approximate Counting and Integration_ , page 482–520. PWS Publishing Co., USA, 1996. 

- Deddy Jobson and Yilin Li. Investigating the potential of using large language models for scheduling. In _AIWare_ , pages 170–171, 2024. 

- Sham Kakade and John Langford. Approximately optimal approximate reinforcement learning. In _ICML_ , 2002. 

- Adam Tauman Kalai and Santosh Vempala. Simulated annealing for convex optimization. _MOR_ , 31(2):253–266, 2006. 

- Scott Kirkpatrick, C Daniel Gelatt Jr, and Mario P Vecchi. Optimization by simulated annealing. _Science_ , 220(4598):671–680, 1983. 

- László Lovász and Santosh Vempala. Simulated annealing in convex bodies and an _O_<sup>_∗_</sup> ( _n_<sup>4</sup> ) volume algorithm. _JCSS_ , 72(2):392–417, 2006. 

38 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

- Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative refinement with self-feedback. In _NeurIPS_ , 2023. 

- Hongyuan Mei, Mohit Bansal, and Matthew Walter. Listen, attend, and walk: Neural mapping of navigational instructions to action sequences. In _AAAI_ , 2016. 

- Kerrie L Mengersen and Richard L Tweedie. Rates of convergence of the Hastings and Metropolis algorithms. _Ann. Stat._ , 24(1):101–121, 1996. 

- William Merrill and Ashish Sabharwal. The expressive power of transformers with chain of thought. In _ICLR_ , 2024. 

- Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller, and Edward Teller. Equation of state calculations by fast computing machines. _J. Chem. Phys._ , 21: 1087–1092, 1953. 

- Tom Minka. Divergence measures and message passing. Technical Report MSR-TR-2005-173, January 2005. 

- Rémi Munos. Optimistic optimization of a deterministic function without the knowledge of its smoothness. In _NIPS_ , pages 783–791, 2011. 

- Radford M. Neal. Annealed importance sampling, 1998. URL https://arxiv.org/abs/physics/ 9803008. 

- OpenAI. Introducing OpenAI o1-preview. https://openai.com/index/ introducing-openai-o1-preview/, 2024. 

- Matthew D. Parno and Youssef M. Marzouk. Transport map accelerated markov chain monte carlo. _SIAM/ASA Journal on Uncertainty Quantification_ , 6(2):645–682, 2018. doi:10.1137/17M1134640. 

- Jan Peters and Stefan Schaal. Reinforcement learning by reward-weighted regression for operational space control. In _ICML_ , pages 745–750, 2007. 

- Jan Peters, Katharina Mülling, and Yasemin Altun. Relative entropy policy search. In _AAAI_ , pages 1607–1612, 2010. 

- S.A. Piyavskii. An algorithm for finding the absolute extremum of a function. _USSR Comp. Math. Math. Phys._ , 12(4):57–67, 1972. ISSN 0041-5553. doi:https://doi.org/10.1016/00415553(72)90115-2. URL https://www.sciencedirect.com/science/article/pii/ 0041555372901152. 

- Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving language understanding by generative pre-training. _OpenAI report_ , 2018. https://cdn.openai.com/ research-covers/language-unsupervised/language_understanding_paper.pdf. 

- Reuven Rubinstein. The cross-entropy method for combinatorial and continuous optimization. _MCAP_ , 1:127–190, 1999. 

39 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

- Daniel Russo and Benjamin Van Roy. Learning to optimize via posterior sampling. _MOR_ , 39(4): 1221–1243, 2014. 

- Clayton Sanford, Bahare Fatemi, Ethan Hall, Anton Tsitsulin, Mehran Kazemi, Jonathan Halcrow, Bryan Perozzi, and Vahab Mirrokni. Understanding transformer reasoning capabilities via graph algorithms. In _NeurIPS_ , 2024. 

- John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. Trust region policy optimization. In _ICML_ , 2015. 

- Bobak Shahriari, Kevin Swersky, Ziyu Wang, Ryan P Adams, and Nando De Freitas. Taking the human out of the loop: A review of Bayesian optimization. _Proc. IEEE_ , 104(1):148–175, 2016. 

- Bruno O. Shubert. A sequential method seeking the global maximum of a function. _SIAM Journal on Numerical Analysis_ , 9(3):379–388, 1972. ISSN 00361429. URL http://www.jstor.org/stable/ 2156138. 

- Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, and Yarin Gal. AI models collapse when trained on recursively generated data. _Nature_ , 631(8022):755–759, 2024. 

- Jasper Snoek, Hugo Larochelle, and Ryan P Adams. Practical Bayesian optimization of machine learning algorithms. In _NIPS_ , volume 25, 2012. 

- Niranjan Srinivas, Andreas Krause, Sham Kakade, and Matthias Seeger. Gaussian process optimization in the bandit setting: No regret and experimental design. In _ICML_ , 2010. 

- Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei A. Efros, and Moritz Hardt. Test-time training with self-supervision for generalization under distribution shifts. In _ICML_ , 2020. 

- Csaba Szepesvári and Rémi Munos. Finite time bounds for sampling based fitted value iteration. In _ICML_ , page 880–887, 2005. 

- Stefanie Tellex, Thomas Kollar, Steven Dickerson, Matthew Walter, Ashis Banerjee, Seth Teller, and Nicholas Roy. Understanding natural language commands for robotic navigation and mobile manipulation. In _AAAI_ , pages 1507–1514, 2011. 

- Philip Thomas and Emma Brunskill. Data-efficient off-policy policy evaluation for reinforcement learning. In _ICML_ , 2016. 

- Luke Tierney. Markov Chains for Exploring Posterior Distributions. _Ann. Stat._ , 22(4):1701 – 1728, 1994. 

- A. W. van der Vaart. _Asymptotic Statistics_ . Cambridge Series in Statistical and Probabilistic Mathematics. Cambridge University Press, 1998. 

- L. G. Valiant. A theory of the learnable. _CACM_ , 27(11):1134–1142, 1984. 

- Michal Valko, Alexandra Carpentier, and Rémi Munos. Stochastic simultaneous optimistic optimization. In _ICML_ , pages 19–27, 2013. 

40 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

- A. W. van der Vaart and J. H. van Zanten. Rates of contraction of posterior distributions based on gaussian process priors. _Ann. Stat._ , 36(3):1435–1463, 2008. 

- Roman Vershynin. _High-Dimensional Probability: An Introduction with Applications in Data Science_ . Cambridge University Press, 2018. 

- Heng Wang, Shangbin Feng, Tianxing He, Zhaoxuan Tan, Xiaochuang Han, and Yulia Tsvetkov. Can language models solve graph problems in natural language? In _NeurIPS_ , 2023. 

- R. Wong. _Asymptotic Approximations of Integrals_ . Society for Industrial and Applied Mathematics, 2001. doi:10.1137/1.9780898719260. URL https://epubs.siam.org/doi/abs/10.1137/1. 9780898719260. 

Tengyang Xie, Dylan J. Foster, Yu Bai, Nan Jiang, and Sham M. Kakade. The role of coverage in online reinforcement learning. In _ICLR_ , 2023. 

## **Appendix A. Additional Discussion on ALDRIFT and Coarse Learnability** 

### **A.1. Connecting TOPIFT to ALDRIFT** 

Recall TOPIFT from Algorithm 1. We now describe a smooth approximation of TOPIFT that avoids the hard selection of the _m_ smallest-cost samples, and show that this naturally leads to a procedure akin to ALDRIFT. 

Towards this end, we position TOPIFT within a framework in which the algorithm tries to make the distribution _Lr_ a progressively good approximation to the distribution _p_<sup>_∗_</sup> _T_<sup>.Unfortunately,</sup> obtaining a closed form for _Lr_ in TOPIFT seems difficult because we choose the samples with the smallest _d_ ( _·_ ), i.e., hard-min. To circumvent this difficulty, we will use a soft-min distribution to approximate this step; this leads to a simulated annealing algorithm that we describe next. 

- Note that the construction of _Sr_<sup>_′_in Algorithm 1 can be split into two steps:</sup> 

1. We generate _s_ from the distribution _Lr−_ 1. If this is repeated _m · M_ times, this corresponds to generating _Sr_ . 

2. We select the samples from _Sr_ with a minimum _d_ ( _·_ ). This can be smoothly approximated by keeping each _s ∈ Sr_ with probability _e_<sup>_−τr·d_(</sup><sup>_s_)</sup> . This is a “soft-min” that favors solutions _s_ with smaller _d_ ( _s_ ). The parameter _τr_ can be chosen so that if _D_ = max _s∈S d_ ( _s_ ), then _τr_ =<sup><u>ln</u></sup> _D_<sup>_<u>M</u>_.This ensures that any</sup><sup>_s∈S_is sub-selected in this step with probability at least</sup> _M_ <u>1</u><sup>, so that E[</sup><sup>_|S_</sup> _r_<sup>_′|_]</sup><sup>_≥m_.</sup> 

Therefore, the sampling distribution of _Sr_<sup>_′_is proportional to</sup><sup>_Lr−_1(</sup><sup>_s_)</sup><sup>_· e−τr·d_(</sup><sup>_s_).If we assume</sup> that _Lr_ is faithfully learned from these samples, we obtain _Lr_ ( _s_ ) _∝L_ ( _s_ ) _· e_<sup>_−_�</sup> _t_<sup>_r_</sup> =1<sup>_τt·d_(</sup><sup>_s_)</sup> . We can now choose the number of iterations _Q_ so that<sup>�</sup><sup>_Q_</sup> _t_ =1<sup>_τt≈T_,whichleadstothedistribution</sup><sup>_pT_.</sup> This yields a smoothed variant of TOPIFT, analogous to simulated annealing, where the temperature _τ_ =<sup>�</sup><sup>_r_</sup> _t_ =1<sup>_τt_is gradually increased across iterations and a model</sup><sup>_pτ_is learned. The gradual increase</sup> ensures that the set _Sr_<sup>_′_at each iteration remains sufficiently large.</sup> 

A key challenge is that in each iteration, the model _Lr_ only approximates the sampling distribution _Sr_<sup>_′_.Thisapproximationcanbequitecrude,sincethedistribution</sup><sup>_pτ_(</sup><sup>_s_)</sup><sup>_∝L_(</sup><sup>_s_)</sup><sup>_· e−τ·d_(</sup><sup>_s_)</sup> encodes combinatorial constraints that the model cannot fully capture, even with many samples. Consequently, errors can accumulate multiplicatively across fine-tuning iterations, making it difficult to formally prove convergence for the simple heuristic. We address this issue by incorporating 

41 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

a Metropolis–Hastings step to select the top samples. This allows the approximately learned model _Lr−_ 1 to serve as an efficient proposal distribution, while the acceptance rule ensures sampling from the true target distribution _pτ_ , preventing error accumulation. This leads to the ALDRIFT algorithm. 

### **A.2. Necessity of the Metropolis Step in ALDRIFT** 

In ALDRIFT, we note that it is essential to sample from the true target _pτ_ at each iteration _τ_ rather than from a reweighted approximation. If one were to draw samples _Sτ_ directly from _Lτ −_ and re-weight them by _e_<sup>_−d_(</sup><sup>_s_)</sup><sup>_/D_</sup> , the resulting distribution would differ from _pτ_ ( _s_ ) _∝ pτ −_ ( _s_ ) _e_<sup>_−d_(</sup><sup>_s_)</sup><sup>_/D_</sup> by a multiplicative factor, causing this error to compound across iterations as _τ_ increases. The Metropolis–Hastings step avoids this accumulation by producing samples that are asymptotically distributed according to _pτ_ , ensuring that the fine-tuned model _Lτ_ is trained on unbiased samples at every iteration. 

It is also tempting to ask whether simple rejection sampling could replace the Metropolis– Hastings step. In our setting, however, the target distribution at temperature _τ_ has unnormalized weight _p_ ˜ _τ_ ( _s_ ) = _L_ 0( _s_ ) _e_<sup>_−τd_(</sup><sup>_s_)</sup> with normalizing constant _Zτ_ =<sup>�</sup> _s_<sup>_p_˜</sup><sup>_τ_(</sup><sup>_s_).Because the target dis-</sup> tribution concentrates into an exponentially small volume as _τ_ grows, we have _p_ ˜ _τ_ ( _s_ ) _≪Lτ −_ ( _s_ ) almost everywhere in the domain. Consequently, one cannot simply estimate _Zτ_ empirically by drawing samples from the proposal _Lτ −_ ; the vast majority of proposals will fall in regions where the target mass is negligible, causing the variance of the estimator to explode. Any empirical estimate would be grossly inaccurate without exponentially many draws. Finding a reasonably tight bound on _Zτ_ is typically not possible unless we make specific structural assumptions (as we do for the distributions in Section 5). The Metropolis–Hastings update avoids this dependence because the global normalizer cancels from its acceptance ratio; it depends only on relative density ratios between successive states. As a result, under coarse learnability the acceptance probabilities remain polynomially bounded on the typical set, and the chain mixes in polynomial time regardless of how small _Zτ_ becomes. 

### **A.3. ALDRIFT vis–a–vis Model Reference Adaptive Search (MRAS)** 

Our analysis of ALDRIFT can be interpreted as a finite-sample robustification of the model reference adaptive search (MRAS) framework (Hu et al., 2007) via the Metropolis–Hastings proposal step. In the MRAS framework, one defines a sequence of ideal target distributions, _gk_ ( _s_ ), and updates a parametric model _f_ ( _·_ ; _θk_ ) to approximate _gk_ by minimizing the KL-divergence _D_ KL( _gk∥fθ_ ). In our instantiation, _gk_ ( _s_ ) _∝L_ 0( _s_ ) _e_<sup>_−τkd_(</sup><sup>_s_)</sup> . 

Standard MRAS theory guarantees _f_ ( _·_ ; _θk_ ) converges to a point mass at the globally optimal solution for _d_ . However, this analysis relies both on exactly updating the parameter _θ_ via infinite samples as well as the specific structural properties of natural exponential families to ensure the optimum always remains within the support of this generated distributions (Hu et al., 2007). Therefore, this theory does not provide explicit sample complexity bounds. In the finite-sample regime, projecting a complex target _pτ_ onto a generative model introduces empirical errors. Without specific statistical guarantees, there is no assurance that a polynomial number of samples suffices to maintain coverage of the optimal region, and as mentioned before, this aspect may break the algorithm. 

Our framework identifies the statistical assumption (coarse learnability) and algorithmic modification (utilizing the coarse generative model as a proposal for Metropolis–Hastings rather than 

42 

SAMPLE-EFFICIENT OPTIMIZATION OVER GENERATIVE PRIORS VIA COARSE LEARNABILITY 

sampling from it directly) needed for achieving polynomial sample complexity in classical MBO. While methods like MRAS rely on the rigid geometry of exponential families to guarantee support preservation, Assumption 2 requires that the learner captures the target’s mass within a polynomial factor. Our framework therefore shifts the burden from architectural correctness (choosing the right parametric family) to statistical expressivity (learning a cover), making the theory applicable to settings where exact parametric alignment is impossible. We presented a simple case of such model mis-match in Section 7.1. 

## **Appendix B. Prompts for Empirical Results** 

### **Finding Cycle in a Graph** 

"""Identify a cycle of length exactly {k} in this undirected graph. Edges: {edges} Think step by step. Finally the last line of your response must be the final output. The last line MUST be a list like [0,1,2,...,0] or ’No cycle found’. No other text:""" 

### **Line Scheduling** 

""" There are {n} museums on a line. They are numbered from 0 to {m}. I’m currently located at museum 0 and the current timestamp is 0. I want to visit all these museums one by one in a sequence. Each museum has an opening time. If I reach a particular museum before it opens then I may have to wait. The opening times for the museums are as follows: 

[ **opening times go here** ] 

In addition, the following list of {m} numbers contains the time to travel from museum i to i+1. So the first number is the time to travel from 0 to 1 and so on: 

[ **travel times go here** ] 

Finally, I have certain constraints in terms of the minimum and maximum amount of time I want to visit each museum. This is described as the following list of arrays: 

- [ **constraints go here** ] 

Give me a schedule in terms of a list of {n} numbers describing how much time I should spend at each place so that all my constraints are satisfied and at the same time my total wait time is as little as possible. Do not use code. Simply output the list of {n} numbers (one per line) and nothing else.""" 

### **Spanning Tree** 

"""You are given a graph with vertices labeled from 0 to {num_vertices-1}. Each line below lists an edge of the graph as (i,j). 

- [ **edges go here** ] 

Your goal is to output a list of H of a subset of the edges that form a spanning tree, i.e., the subgraph induced by H should be connected. Furthermore, each vertex should appear in at most {deg} times in the list. Simply output the list of edges and nothing else. Format your answer by producing one edge per new line.""" 

43 

AWASTHI GOLLAPUDI KUMAR MUNAGALA 

## **Appendix C. Acknowledgment of Generative AI Use** 

We utilized Gemini 3.1 Pro to assist with (1) identifying connections to model-based optimization in Appendix A.3; (2) identifying relevant literature to simplify the proof of Theorem 1; (3) improving comparisons to prior work by finding citations; and (4) generating the code for the experiments in Section 6. We also benefited from discussions with the model, which helped suggest possible approaches to proving the results in Sections 5 and 7.3. All results, including citations and algebra, were verified by the authors, who take full responsibility for the paper’s accuracy and contributions. 

44 

