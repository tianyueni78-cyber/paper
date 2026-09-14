# **Rethinking LLM-Driven Heuristic Design: Generating Efficient and Specialized Solvers via Dynamics-Aware Optimization** 

Rongzheng Wang<sup>1</sup> , Yihong Huang<sup>1</sup> , Muquan Li<sup>1</sup> , Jiakai Li<sup>1</sup> , Di Liang<sup>2</sup> , Bob Simons<sup>2</sup> , Pei Ke<sup>1</sup> , Shuang Liang<sup>1*</sup> , Ke Qin<sup>1</sup> 

1 University of Electronic Science and Technology of China 

2 Tencent Hunyuan 

wangrongzheng@std.uestc.edu.cn shuangliang@uestc.edu.cn 

## **Abstract** 

Large Language Models (LLMs) have advanced the field of Combinatorial Optimization through automated heuristic generation. Instead of relying on manual design, this LLMDriven Heuristic Design (LHD) process leverages LLMs to iteratively generate and refine solvers to achieve high performance. However, existing LHD frameworks face two critical limitations: (1) Endpoint-only evaluation, which ranks solvers solely by final gap to a reference solution, ignoring the convergence process and runtime efficiency; (2) High adaptation costs, where distribution shifts necessitate re-adaptation to generate specialized solvers for heterogeneous instance groups. To address these issues, we propose Dynamics-Aware Solver Heuristics (DASH), a framework that co-optimizes solver search mechanisms and runtime schedules guided by a convergenceaware metric, thereby identifying efficient and high-performance solvers. Furthermore, to mitigate expensive re-adaptation, DASH incorporates Profiled Library Retrieval (PLR), which maintains group-specialized solvers for profileaware warm starts. These solvers are archived concurrently during evolution, allowing DASH to reuse matched specialists across heterogeneous distributions without restarting adaptation. Experiments on four combinatorial optimization problems demonstrate that DASH improves runtime efficiency by over 4 _×_ while outperforming prior LHD baselines in the overall balance between gap and runtime across diverse problem scales. Furthermore, by enabling profile-aware warm starts, DASH maintains lower gap under distribution shift while reducing LLM adaptation costs by about 90%. 

## **1 Introduction** 

Many fundamental problems in computing and engineering, including routing, scheduling, and chip placement, are combinatorial optimization problems (Korte and Vygen, 2008). In practice, 

high-performance solvers for these problems rely on carefully hand-crafted heuristics (Burke et al., 2013). Due to the extensive search space, executing such heuristic solvers is computationally expensive. Beyond the high design cost, these heuristics often struggle with generalization: when the instance distribution changes (e.g., in size or density), sustaining performance typically requires re-design for re-adaptation (Wolpert and Macready, 1997). 

LLM-Driven Heuristic Design (LHD) (Yao et al., 2025; Wu et al., 2025) alleviates this burden by automatically generating and improving solvers. Recent works have advanced this domain by establishing a fundamental iterative workflow in which LLMs generate candidate solvers, evaluate them through execution feedback, and select promising ones for further refinement (e.g., FunSearch (Romera-Paredes et al., 2024), EoH (Liu et al., 2024), and ReEvo (Ye et al., 2024)). However, the evaluation process requires repeatedly generating and executing time-consuming solvers, meaning that practical LHD still faces two key challenges. 

**Challenge 1: Generating efficient solvers** Most LHD frameworks (Zheng et al., 2025; Dat et al., 2025) select candidate solvers only by the final score (e.g., gap to an optimal or best-known value), thereby ignoring a key dimension: the convergence trajectory within the time. Crucially, early convergence often indicates the potential to further reduce the gap to the optimal (Hansen and Zilberstein, 1996), yet comparable final score makes it difficult to distinguish such efficient solvers. Some recent efficiency-aware LHD works have started to incorporate time objectives in solver selection (e.g., MEoH (Yao et al., 2025)). Nevertheless, relying solely on such efficiency signal fails to capture the convergence dynamics (e.g., early convergence, stable improvement, and long stagnation). As Figure 1 (left) shows, three solvers reach comparable final 

1 



<!-- Start of picture text -->
Size Transfer Density Transfer<br>20 Solver 1 | Current gap trajectory | Early convergence 20Solver 1 | Best-so-far gap trajectory | Early convergence Cell: Relative gap (lower is better) Cell: Relative gap (lower is better)<br>1510 1510 20 (native)1.00x (+20%)1.20x (+100%)2.00x (+180%)2.80x (+250%)3.50x 2.5 [1,2] (native)1.00x (+12%)1.12x (+28%)1.28x (+45%)1.45x (+62%)1.62x 0.6<br>5 5 2.0 0.5<br>200Solver 2 | Current gap trajectory | Stable improvement 20Solver 2 | Best-so-far gap trajectory | Stable improvement0 50 (+15%)1.15x (native)1.00x (+65%)1.65x (+120%)2.20x (+180%)2.80x (2,3] (+10%)1.10x (native)1.00x (+15%)1.15x (+30%)1.30x (+48%)1.48x 0.4<br>15 15 1.5<br>10 10 100 (+30%)1.30x (+18%)1.18x (native)1.00x (+50%)1.50x (+85%)1.85x (3,4] (+18%)1.18x (+9%)1.09x (native)1.00x (+18%)1.18x (+34%)1.34x 0.3<br>50 50 1.0<br>20 Solver 3 | Current gap trajectory | Long stagnation 20 Solver 3 | Best-so-far gap trajectory | Long stagnation 200 (+55%)1.55x (+40%)1.40x (+22%)1.22x (native)1.00x (+28%)1.28x (4,5] (+26%)1.26x (+18%)1.18x (+10%)1.10x (native)1.00x (+16%)1.16x 0.2<br>15 15 0.5<br>10 10 0.1<br>5 5 500 (+75%)1.75x (+62%)1.62x (+35%)1.35x (+15%)1.15x (native)1.00x (5,6] (+34%)1.34x (+27%)1.27x (+18%)1.18x (+8%)1.08x (native)1.00x<br>0 0 2 4 Time (s) 6 8 10 0 0 2 4 Time (s) 6 8 10 20 50 100 200 500 0.0 [1,2] (2,3] (3,4] (4,5] (5,6] 0.0<br>Eval group Eval group<br>Gap (%)<br>Gap (%) Train group Train group<br>Extra degradation ratio Extra degradation ratio<br>Gap (%)<br><!-- End of picture text -->

Figure 1: **Motivating Experiments on TSP tasks using Guided Local Search (Voudouris and Tsang, 1999) as solver backbone and under a 10s time limit.** ( _Left_ ) Three solvers reach similar final gaps despite different trajectories, rendering them nearly indistinguishable under endpoint-only evaluation. Solver 1 converges earlier, achieving lower gaps at earlier times and thereby leaving more of the time budget for subsequent improvements. ( _Right_ ) Performance significantly degrades when solvers are transferred across shifts in problem size (node count) or density (node clustering), further underscoring the necessity of generating specialized solvers for distinct instance distributions. 

### gaps with different trajectories, rendering them indistinguishable under endpoint-only evaluation. 

**Challenge 2: Generating specialized solvers** LHD is costly as it requires repeatedly refining solvers on training instances (Guo et al., 2025). Some methods reduce this cost by reusing information from prior evaluations to filter redundant candidates, thereby cutting down solver runs (e.g., Hercules (Wu et al., 2025)). However, real-world instances are heterogeneous: a solver that works well on one instance group may degrade under distribution shifts in scale or other instance characteristics (Rice, 1976). Consequently, maintaining performance across diverse groups requires groupwise adaptation, leading to repeated LLM-driven iteration. Although prior work lowers cost per iteration, it remains inefficient under distribution shifts. As Figure 1 (right) illustrates, solvers optimized for one instance group can degrade significantly on another, resulting in costly re-adaptation. 

These observations underscore the necessity of assessing a solver by the temporal evolution of its solution quality, framing execution as a dynamical process. Accordingly, we propose DynamicsAware Solver Heuristics ( **DASH** ), a framework that improves solver performance and efficiency by optimizing how the solver searches and how it spends runtime. Under this view, we decompose solver design into the search mechanism (e.g., update rules and guidance design) and the runtime schedule (e.g., time allocation across phases). To quantify these dynamics, we introduce the Trajectory-aware Lyapunov Decay Rate ( **tLDR** ) (Khalil and Grizzle, 2002), which measures the rate and consistency of convergence and guides the co-evolution of search 

### mechanism and runtime schedule in DASH. 

To mitigate re-adaptation costs, DASH further incorporates Profiled Library Retrieval ( **PLR** ). PLR decouples archiving from evolution: within a single evolutionary process, it archives group-specific solvers, while continuing to evolve the global solver based on average performance. This strategy builds a diverse library within a single search and enables cost-effective profile-aware warm starts. We validate DASH on four combinatorial optimization problems and demonstrate its generalizability across solver backbones. Results show that DASH improves runtime efficiency by over 4 _×_ while outperforming prior LHD baselines in the overall balance between gap and runtime. By enabling profile-aware warm starts, DASH maintains lower gap under distribution shift while reducing LLM adaptation costs by about 90%. 

Our contributions can be summarized as follows: 

- We introduce the tLDR, a trajectory-aware metric that shifts evaluation from static endpoints to dynamic convergence efficiency, prioritizing fast and stable solvers. 

- We propose DASH, a framework that coevolves search mechanisms and runtime schedules. It incorporates Profiled Library Retrieval (PLR) to maintain specialized solvers for cost-effective profile-aware warm starts. 

- We validate DASH on four combinatorial optimization problems. Results show that it improves runtime efficiency by over 4 _×_ while outperforming LHD baselines in the overall balance between gap and runtime, and substantially reduces adaptation cost under distribution shift. 

2 

## **2 Related Work** 

**Real-World Combinatorial Optimization.** Combinatorial optimization plays a central role in realworld decision systems (Korte and Vygen, 2008), where routing, dispatching, scheduling, and resource allocation must be performed under strict operational constraints. In such settings, optimization is valuable not only because it improves solution quality, but also because it directly affects service efficiency, resource utilization, and system responsiveness. At the same time, practical deployments are complicated by dynamic arrivals, limited runtime budgets, and heterogeneous instance distributions. These challenges have been widely studied across a range of real-world applications, including route guidance and taxi services (Yuan et al., 2013a,b), constrained route queries (Li et al., 2013), large-scale dispatching (Tong et al., 2023), airport ground handling (Zhou et al., 2023), ridehailing control (Zhang et al., 2024), and dynamic routing (Zhang et al., 2025). Real-world optimization is inherently context-dependent, and therefore calls for adaptive methods that can respond to varying instances and runtime constraints rather than relying on a single fixed solver. 

**Heuristics and Solver Adaptation.** Classical combinatorial optimization has long relied on problem-specific heuristics and metaheuristics (Korte and Vygen, 2008), whose effectiveness often depends on carefully designed rules tailored to a solver and a problem family. Hyper-heuristics raise this level of generality by seeking to automate the selection or generation of heuristics across problem classes (Burke et al., 2013). However, they still face persistent challenges: heuristic quality can vary substantially across instances, and good decisions often depend on available runtime as well as final solution quality. This has motivated a related research direction on instance-aware solver adaptation, including algorithm selection (Rice, 1976; Lindauer et al., 2015) and runtime-aware control inspired by anytime optimization (Hansen and Zilberstein, 1996; Zilberstein, 1996), where the preferred solver or configuration changes with instance characteristics and budget regimes. These limitations have motivated recent LLM-driven approaches that attempt to automate heuristic discovery while retaining the flexibility needed for heterogeneous optimization scenarios. 

**LLM-Driven Heuristic Design.** Combinatorial optimization problems typically rely on heuris- 

tic solvers (Garey and Johnson, 1983). Recently, LLMs have advanced LLM-Driven Heuristic Design (LHD) by establishing an iterative generate, evaluate, and select workflow to synthesize and refine solvers (Guo et al., 2025; Zheng et al., 2025; Dat et al., 2025). Notable frameworks include FunSearch (Romera-Paredes et al., 2024), which couples program mutation with evolutionary search based on execution feedback; EoH (Liu et al., 2024), which co-evolves natural language ideas and code implementations; and ReEvo (Ye et al., 2024), which employs reflective prompts to guide the search. However, most LHD methods select solvers solely based on endpoint metrics, ignoring the convergence process. Although some efficiency-aware variants incorporate runtime objectives, they typically reduce the dynamic trajectory to a few aggregated statistics (Yao et al., 2025). A complementary direction addresses evaluation costs by reusing mechanisms or predictor-based pruning to filter candidates (Wu et al., 2025; Guo et al., 2025). Although effective for reducing overhead, such pruning may limit search diversity and overlook promising solvers. DASH addresses these limitations by optimizing the full convergence trajectory for efficiency and employing PLR for cost-effective adaptation. This allows archived specialists to be reused across heterogeneous instance profiles without re-evolving a separate solver for each profile group. 

## **3 Method** 

### **3.1 Solver Runs as Time-Evolving Trajectory** 

We adopt a dynamical systems view of solver execution under a time limit _T_ . For an instance _x_ , a solver _π_ = ( _θ, σ_ ) induces a time-evolving solution trajectory _z_ ( _τ_ ) _∈Z_ ( _x_ ), where _θ_ encodes the search mechanism (e.g., update rules and guidance design) and _σ_ encodes the runtime schedule (e.g., time allocation across phases). In practice, solvers update their solutions in discrete steps, so we denote by _zk_ := _z_ ( _τk_ ) the solver state at cumulative runtime _τk_ , and consider: 



where _F_ ( _·_ ; _x, θ, σ_ ) denotes the state transition induced by solver _π_ = ( _θ, σ_ ) on instance _x_ , and ∆ _τk_ is the measured time cost of step _k_ . 

3 

### **3.2 Lyapunov Potential and Incumbent Trajectory** 

**Lyapunov potential definition.** To compare such trajectories across runs, we require a progress signal that measures the distance to a target solution _z_<sup>_⋆_</sup> (e.g., an optimal or best-known solution) at each time. In dynamical systems, Lyapunov functions formalize this idea as a generalized energy that is minimized at the target state (Khalil and Grizzle, 2002). Adopting this perspective, we define a proxy potential _V_ : _Z_ ( _x_ ) _→_ R _≥_ 0 satisfying: 



**Incumbent trajectory.** For a minimization objective _fx_ ( _·_ ) with reference optimum _f_<sup>_⋆_</sup> (exact or bestknown), we measure the distance to optimality via the relative gap: gap _x_ ( _τ_ ) = � _fx_ ( _z_ ( _τ_ )) _− fx_<sup>_⋆_</sup> � _/|fx_<sup>_⋆|_.</sup> Consistent with Eq. (2), we set the time-dependent residual as the gap itself: 



where _V_ ( _τ_ ) is short for _V_ ( _z_ ( _τ_ )). Since heuristic search trajectories are typically stochastic and nonmonotone, we extract persistent progress via the incumbent (best-so-far) trajectory: 



By construction, _V_ best( _τ_ ) is non-increasing, providing a monotone progress signal that aligns with an energy-descent view of optimization dynamics. 

We then project the incumbent trajectory into logarithmic space to obtain a scale-consistent notion of progress. In particular, many improvements in combinatorial optimization are naturally compared in relative terms (i.e., multiplicative reductions of the gap). Working in log space turns such multiplicative changes into additive decreases, making progress comparable across different residual magnitudes. To ensure well-defined values even when the optimum is reached (i.e., _V_ best = 0), we employ a numerical lower bound _δ >_ 0: 



We use _ℓ_ ( _T_ ) as the corresponding terminal logresidual under the time limit _T_ . 

### **3.3 Trajectory-aware Lyapunov Decay Rate** 

Previous LHD methods based solely on the terminal gap at time _T_ fail to capture optimization 

dynamics: two solvers may achieve similar _ℓ_ ( _T_ ) while exhibiting different early progress and different persistence in low-residual regimes. To summarize the incumbent evolution over the entire process, we compute the time-averaged log-residual: 



A smaller _J_ ( _T_ ) implies that the solver stays in low-residual states for a larger fraction of time, reflecting both early improvement and sustained convergence. 

To convert this trajectory-aggregated quantity into an interpretable decay rate, we derive an effective slope. Specifically, we define an equivalent linear trajectory _ℓ_<sup>˜</sup> ( _τ_ ) = _ℓ_ (0) _− kτ_ , anchored at the initial residual _ℓ_ (0). We determine the decay slope _k_ by requiring that this hypothetical linear path yields the same time-averaged value _J_ ( _T_ ) as the actual observed run over [0 _, T_ ]. 

The integral of this linear path is _Tℓ_ (0) _−_<sup><u>1</u></sup> 2<sup>_kT_2.</sup> By equating this to observed integral _TJ_ ( _T_ ) and solving for _k_ , we define the **Trajectory-aware Lyapunov Decay Rate (tLDR)** : 



tLDR( _T_ ) is the effective decay slope of the incumbent log-residual trajectory over the interval [0 _, T_ ] induced by the time-averaged log-residual _J_ ( _T_ ). Equivalently, it is the constant slope of a linear surrogate _ℓ_<sup>˜</sup> ( _τ_ ) = _ℓ_ (0) _− kτ_ whose timeaverage matches the overall run. A larger tLDR indicates faster and more sustained reduction in logresidual throughout the entire interval [0 _, T_ ], rather than progress concentrated only near the end. For fair comparison, _ℓ_ (0) is always measured from the same initial state for each instance, reused across solver evaluations. 

In practice, tLDR is computed from logged incumbent traces by averaging the incumbent log-residual over wall-clock time and converting that average into an equivalent constant decay slope. Concretely, given a logged incumbent trace _{_ ( _τj, zj_ ) _}_<sup>_m_</sup> _j_ =0<sup>with 0=</sup><sup>_τ_0</sup><sup>_<· · ·<τm_=</sup><sup>_T_and</sup> _ℓj_ = _ℓ_ ( _τj_ ) = ln max � _V_ ( _zj_ ) _, δ_ �, we use the following piecewise-constant form: 



4 

Table 1: Search Mechanism ( _θ_ ) and Runtime Schedule ( _σ_ ) in GLS for TSP. 

|**Component**|**Search Mechanism**_θ_|**Runtime Schedule**_σ_|
|---|---|---|
|Initialization|tour construction (fixed for fairness)|(none; fixed single start)|
|Neighborhood|candidate restriction and move neighborhood def-<br>inition|when to update / switch|
|Local improvement|move operators and acceptance logic|phase budgets and iteration/stop caps|
|Guidance|guidance/penalty rule and how it interacts with<br>search|when to activate and how often to update|
|Perturbation|perturbation operator|triggering/frequency and (optional) intensity|
|Stopping|(none)|time cap and stagnation-based stopping|



which gives the corresponding discrete form of tLDR: 



### **3.4 Three Iteration Layers** 

The performance of a solver is governed by two interacting components: the mechanism _θ_ and the schedule _σ_ . However, directly optimizing _π_ = ( _θ, σ_ ) is challenging due to their complex coupling. To address this, we decompose optimization into three sequential layers. Across all layers, we employ a unified protocol based on the terminal log-residual _ℓ_ ( _T_ ), trajectory efficiency tLDR( _T_ ), and (for runtime schedule optimization) solver runtime _t_ run. 

However, heuristic search trajectories can be stochastic and highly dependent on specific instance characteristics. To obtain a stable evaluation signal, candidates are evaluated on a sampled batch _B_ . Acceptance decisions are based on the batch-averaged metrics: terminal log-residual _ℓ_<sup>¯</sup> , trajectory efficiency _k_<sup>¯</sup> (mean tLDR( _T_ )), and runtime _t_ ¯. Lower is better for _ℓ_ ¯ and _t_ ¯, whereas higher is better for _k_<sup>¯</sup> . Each candidate is compared only with its direct parent on the same evaluation batch. We use a shared comparison margin _ϵ_ across all three layers. A metric _x_<sup>_′_</sup> is treated as being within the comparison margin of its parent value _x_ if: 

of _θ_ based on the parent and its evaluation feedback. We then evaluate _θ_<sup>_′_</sup> under a hierarchical selection criterion relative to its parent. A candidate is accepted if it achieves a lower batch-averaged terminal log-residual _ℓ_<sup>¯</sup> ; when _ℓ_<sup>¯</sup> remains within the comparison margin of the parent, we accept the candidate only if it also achieves a sufficiently larger batch-averaged trajectory efficiency _k_<sup>¯</sup> according to the parent-relative criterion. 



### **3.4.2 Mechanism Consolidation Layer (MCL)** 

MCL controls the structural complexity of the evolving mechanism _θ_ . Iterative evolution can lead to code bloat, where the mechanism accumulates brittle logic that overfits to specific instances. In this layer, the LLM refactors the mechanism by rewriting the code structure (e.g., merging duplicated branches and removing dead or redundant logic) while keeping its intended behavior. We employ a preservation criterion: a consolidated candidate _θ_<sup>_′_</sup> is accepted only if both the batch-averaged terminal log-residual _ℓ_<sup>¯</sup> and the batch-averaged trajectory efficiency _k_<sup>¯</sup> remain within the comparison margin of the parent. 



Since _ℓ_<sup>¯</sup> is defined in log space, absolute differences already correspond to relative changes in the underlying residual, whereas _k_<sup>¯</sup> and _t_<sup>¯</sup> are compared on their original scales using parent-relative margins. 

### **3.4.1 Mechanism Discovery Layer (MDL)** 

MDL updates the mechanism _θ_ while keeping the schedule _σ_ fixed. In each iteration, the LLM produces a candidate mechanism _θ_<sup>_′_</sup> by editing the code 

### **3.4.3 Schedule Shaping Layer (SSL)** 

SSL updates the schedule _σ_ while keeping the mechanism _θ_ fixed. The _σ_ specifies how the solver runs over the time budget: which modules are invoked, in what order, and with what triggering rules and per-phase budgets. In each iteration, we provide the LLM with the parent schedule together with its evaluation traces (e.g., per-module runtime 

5 



<!-- Start of picture text -->
Offline Evolution Online Evaluation<br>Part A: tLDR-based selection Part B: DASH Iteration Part C:Profiled Library Retrieval<br>MDL  (Mechanism Discovery Layer) Offline archive Online retrieval<br>NP-hard t LDR( T )<br>instance x LLM instancesTrain ����<br>Code Mutation & Selection<br>Candidate �1<br>(�, �) (�, �) Run solver MCL  (Mechanism Consolidation Layer) Profile<br>(budget T) (�, �) �(����)<br>H1 H2 same budget T LLM ��1<br>De-duplication & Merging<br>�� ��<br>�2<br>Gap% t LDR 1( T ) Gap% t LDR 2( T )   SSL  (Schedule Shaping - Compression)<br>Profile (�, �)<br>J 1 ( T ) J 2 ( T ) …Time LLM Time �(�) ��2 (�, �) Retrieval<br>Time Time Runtime Compression (�0, �0)<br>t LDR( T )  T 2 (0)  J ( T )  SSL  (Schedule Shaping - Enhancement) �3 J 1 ( T )<br>t LDR1( T )  t LDR 2 ( T ) LLM  Module (�, �)<br>Enhancement<br>warm-start<br>select  �� ✓ ��3 run<br><!-- End of picture text -->

Figure 2: **Overview of the DASH framework.** Offline evolution co-evolves the solver across MDL, MCL, and SSL using terminal log-residual and trajectory efficiency for selection. In parallel, PLR maintains group-wise archives from evaluated candidates. At test time, PLR retrieves a group-specific solver to warm-start evaluation. 

and the resulting convergence trajectory), and the LLM proposes a revised schedule _σ_<sup>_′_</sup> by adjusting module allocation and control parameters. We then evaluate _σ_<sup>_′_</sup> under the same protocol as its parent. SSL proceeds in two consecutive stages: it first performs _Compression_ to reduce wasted computational slack, and then applies _Enhancement_ to spend the recovered budget more effectively. 

**Stage 1: Compression** This stage targets computational slack in the execution chain. Given the parent trace, the LLM revises _σ_ by shortening or removing low-efficiency phases and by retuning iteration limits or trigger conditions, so that the solver achieves a comparable batch-averaged terminal logresidual with lower batch-averaged runtime. However, tLDR( _T_ ) is typically compared under the same time budget _T_ . Once compression changes the realized runtime, trajectory comparisons based on tLDR( _T_ ) become mismatched. We therefore use batch-averaged runtime _t_<sup>¯</sup> for schedule-level acceptance in this stage. A compressed schedule is accepted only if it reduces the batch-averaged runtime beyond the comparison margin while keeping the batch-averaged terminal log-residual within the comparison margin of the parent. 



**Stage 2: Enhancement** Once the schedule is compressed, this stage targets marginal gains in terminal log-residual by further modifying _σ_ . Starting from the compressed schedule, the LLM revises _σ_ by reallocating the compressed runtime budget across phases and adjusting runtime schedule controls (e.g., module allocation and their triggering rules or iteration limits), so that more of the runtime is spent on phases that are most helpful for improving the incumbent (e.g., a more thorough perturbation or local-improvement setting). An enhanced schedule is accepted only if it improves the batch-averaged terminal log-residual _ℓ_<sup>¯</sup> beyond the comparison margin and keeps the batch-averaged trajectory efficiency _k_<sup>¯</sup> within the comparison margin of the parent. 



To ground the decomposition of solver edits in a concrete TSP backbone, Table 1 instantiates this decomposition on GLS for TSP by separating editable components into the search mechanism _θ_ and 

6 

the runtime schedule _σ_ . The former specifies the search rules and operators applied by the solver, whereas the latter specifies their activation, frequency, and budget allocation. Accordingly, MDL and MCL revise _θ_ , while SSL edits _σ_ through runtime reallocation and control adjustments. 

## **4 DASH Framework** 

DASH co-evolves the solver mechanism _θ_ and runtime schedule _σ_ via iterative LLM-Driven edits across MDL, MCL, and SSL, and introduces Profiled Library Retrieval (PLR) to decouple archiving from population evolution within a single evolutionary process. We maintain a global population _P_ of top- _k_ solvers ranked by performance aggregated over all groups and a group-wise archive _Lg_ that stores the top- _k_ specialized solvers for each group _g_ . The global population and the group-wise archives serve different objectives in DASH. The global population drives continued evolution toward a solver that remains competitive on average, whereas the group-wise archives preserve specialists that may be suboptimal globally but particularly effective for specific profile regions. 

During evolution, parents are sampled from _P_ . At test time, PLR selects a solver from _Lg_<sup>_⋆_</sup> for profile-aware warm starts. This separation avoids re-evolving a solver for each group and prevents a single archive from being dominated by either global ranking or group specialization in a given batch. For fairness, each evolutionary run starts from the same task-specific initial solver. Figure 2 illustrates the end-to-end DASH workflow. 

### **4.1 Instance Profiles and Instance Groups** 

To improve generalization across heterogeneous instances, we construct an offline training set _D_ train of randomly generated instances with diverse distributions. For each instance _x_ , we compute a lightweight instance profile _ϕ_ ( _x_ ) _∈_ R<sup>_p_</sup> summarizing key size and structural statistics. We then partition _D_ train into _G_ groups _{Dg}_<sup>_G_</sup> _g_ =1<sup>based on</sup> profile similarity, each represented by a prototype _ϕg_ . For routing tasks, these profiles combine scale, distance statistics, and spatial-structure descriptors; for resource-allocation tasks, they summarize value statistics, weight statistics, and capacity tightness across constraints. Within DASH, they are used both to support stratified batch construction during evolution and to index group-specialized solvers for retrieval during evaluation. 

### **4.2 Evaluation and Decoupled Archiving** 

We execute the iterative DASH loop on _D_ train to co-evolve the solver. To efficiently obtain both global and group-specialized solvers, we employ a decoupled archiving strategy. In each iteration, we evaluate candidates on a sampled batch _B_ , composed of batches _Bg_ sampled from each group _Dg_ : 



Each iteration selects a parent solver _π_ = ( _θ, σ_ ) and evaluates the parent together with all candidate solvers on the same union batch. MDL and MCL revise the mechanism _θ_ while keeping the schedule _σ_ fixed, whereas SSL-1 and SSL-2 revise _σ_ while keeping _θ_ fixed. Based on these evaluations, we (i) update the size- _k_ global population using layer-wise acceptance on batch means, replacing the lowest-ranked solver if accepted, and (ii) update each group archive _Lg_ (top- _k_ ) using the candidate’s batch-mean performance on _Bg_ . Archive updates are independent of population acceptance: every evaluated candidate can be inserted into _Lg_ if it outperforms the lowest-ranked entry, keeping only the top- _k_ solvers. Within each archive, candidates are ranked primarily by the recorded group-wise terminal log-residual, with trajectory efficiency and runtime used as secondary criteria. This prioritizes solvers that achieve both strong final quality and efficient convergence under the same evaluation protocol. The decoupling allows a candidate to contribute differently to the two objectives of DASH. A solver that does not remain in the global population may still be preserved if it performs strongly on a particular profile group, whereas a solver with stronger average performance can continue to drive evolution even if it is not the best specialist for every group. 

### **4.3 Online Profiled Library Retrieval (PLR)** 

Given a query instance _x_ new, we compute and normalize its instance profile _ϕ_ ( _x_ new) using the training set statistics. We then identify the most similar group _g_<sup>_⋆_</sup> by minimizing the Euclidean distance to the prototype profiles: 



where _ϕg_ is the prototype profile of group _g_ . Once the best-matching group is identified, we retrieve the best solver ( _θ_<sup>_⋆_</sup> _, σ_<sup>_⋆_</sup> ) from the corresponding group archive _Lg_<sup>_⋆_</sup> and warm-start the new instance 

7 

with a solver specialized to similar profile statistics instead of restarting online re-adaptation. 

### **4.4 DASH configuration.** 

We use GPT-5.4-mini (OpenAI, 2026) with temperature 0.7 as the base LLM for DASH. We set the shared comparison margin _ϵ_ to 0.05 in all experiments. Unless otherwise noted, DASH uses a global population size of 5 and a per-group archive size of 5, and performs 100 solver evaluations during offline evolution. 

## **5 Experiment** 

### **5.1 Experimental Protocol** 

**Datasets and task settings.** We evaluate DASH on four combinatorial optimization tasks: TSP (Liu et al., 2024), CVRP (Uchoa et al., 2017), VRPTW (Solomon, 1987), and MKP (Beasley, 1990). For TSP, we generate synthetic Euclidean instances with _n ∈{_ 20 _,_ 100 _,_ 200 _,_ 500 _}_ nodes by sampling node coordinates independently from [0 _,_ 1] and additionally use TSPLIB as an external benchmark for transfer evaluation. For CVRP, we generate synthetic Euclidean instances with 100 and 500 customers. For VRPTW, we generate synthetic instances with 15 and 20 customers. For MKP, we use OR-Library (Beasley, 1990) benchmark instances with 500 items and 10 and 30 constraints. 

**Training and test construction.** For each task, DASH evolves solvers on a task-specific evolution set and reports final performance on disjoint test instances. For TSP, CVRP, and VRPTW, we generate task-specific synthetic instance pools and split them into an evolution set _D_ train and a held-out test set _D_ test. The evolution set is used for instance profiling, K-means grouping into _G_ =10 groups, and per-iteration batch sampling with _m_ =3 instances per group ( _|B|_ =30), whereas the held-out test set is used only for final reporting. For TSP, TSPLIB is used only for external transfer evaluation. For MKP, DASH is evolved on a separate synthetic training set under the same grouping and batch-construction protocol, while final results are reported only on the selected OR-Library benchmark instances. These benchmark instances are never reused for solver evolution, archive updates, or PLR updates. **Evaluation metrics and reference solutions.** We report _Gap_ and _Time_ , where _Gap_ measures the relative difference to a task-specific reference value and _Time_ is the runtime per instance under the spec- 

ified budget. Lower gap is better for all tasks. The reference value is task-specific: for synthetic TSP, we run Concorde and use the mean objective value over five runs as the reference; for synthetic CVRP and VRPTW, we run PyVRP and use the mean objective value over five runs as the reference; for MKP, we use the best-known values provided by OR-Library, and the reported gap measures the shortfall from these values. 

**Shared solver backbones.** For TSP, we use Guided Local Search (GLS) (Voudouris and Tsang, 1999) as the primary backbone, and additionally instantiate DASH on Iterated Local Search (ILS) (Lourenço et al., 2003) and a Python implementation of LKH (Helsgaun, 2000). For CVRP, VRPTW, and MKP, we use Ant Colony Optimization (ACO) (Dorigo et al., 2006) as the shared backbone. 

**Compared Baselines.** We compare (i) dedicated solvers (Concorde (Cook et al., 2011), LKH3 (Helsgaun), OR-Tools (Perron and Furnon)), (ii) handcrafted heuristics (LS (Aarts and Lenstra, 2018), GLS (Voudouris and Tsang, 1999), KGLS (Arnold and Sörensen, 2019)), (iii) neural combinatorial optimization (NCO) methods (Attention Model (AM) (Kool et al., 2019), POMO (Kwon et al., 2020), Sym-NCO (Kim et al., 2022), DeepACO (Ye et al., 2023), SIL (Luo et al., 2025)), and (iv) LHD frameworks (FunSearch (RomeraParedes et al., 2024), ReEvo (Ye et al., 2024), EoH (Liu et al., 2024), MEoH (Yao et al., 2025), Hercules (Wu et al., 2025)). All LHD baselines use GPT-5.4-mini (OpenAI, 2026), are evaluated under the same task-specific solver budget and wall-clock accounting as DASH within each task, and perform 100 solver evaluations during offline evolution. To preserve fairness while keeping each framework operational, we retain each baseline’s native search workflow whenever it remains compatible with the shared backbone. Accordingly, baseline edits are restricted to mechanism-side heuristic logic on the shared solver skeleton. For CVRP, VRPTW, and MKP, this editable scope covers construction, pheromone, and repair or local-improvement rules under a fixed schedule. DASH additionally optimizes schedule-side controls on top of mechanism updates. 

Our experiments are designed as follows: 

- **RQ1 (Main Results):** How does DASH compare with prior LHD frameworks in solution quality and runtime efficiency across combi- 

8 

Table 2: **Performance comparison on TSP.** We report three metrics: Obj, Gap (%), and Time (s), where Obj denotes the achieved objective value, Gap (%) denotes the percentage difference from the task-specific reference solution, and Time (s) denotes the measured wall-clock runtime per instance. All TSP settings use a 10 s runtime budget per instance. Bold and underlined values indicate the best and second-best LHD results. 

||||TSP 20|||TSP 10|0||TSP 20|0||TSP 50|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method||Obj|Gap (%)|Time (s)|Obj|Gap (%)|Time (s)|Obj|Gap (%|) Time (s)|Obj|Gap (%)|Time (s)|
|**Conventional**<br>||**Solver**||||||||||||
|Concorde||3.827|0.000|0.011|7.763|0.000|0.235|10.652|0.000|1.439|16.553|0.000|7.315|
|LKH3||3.827|0.000|0.021|7.763|0.012|0.622|10.652|0.000|1.984|16.557|0.022|7.784|
|OR-Tools||3.827|0.000|3.002|7.922|2.054|10.002|10.992|3.198|10.004|17.473|5.558|10.012|
|**Heuristic Alg**|**o**|**rithms**||||||||||||
|LS||3.834|0.199|0.003|7.892|1.666|5.301|10.982|3.107|10.000|17.843|7.794|10.067|
|GLS||3.827|0.000|0.095|7.908|1.877|9.861|10.949|2.795|7.067|17.612|6.400|10.114|
|KGLS||3.827|0.000|0.098|7.773|0.136|9.370|10.870|2.053|10.000|17.470|5.541|10.002|
|ILS||3.827|0.000|1.021|7.819|0.722|10.013|10.928|2.604|10.020|17.664|6.711|10.195|
|LKH||3.828|0.022|0.037|7.841|1.005|10.010|10.993|3.208|10.041|17.692|6.880|10.225|
|**NCO**||||||||||||||
|AM||3.832|0.132|0.076|8.101|4.357|0.112|11.403|7.052|9.850|17.119|3.421|10.036|
|POMO||3.827|0.000|0.045|7.766|0.042|0.098|10.777|1.180|9.917|17.688|6.859|9.958|
|SymNCO||3.827|0.000|0.043|7.765|0.035|0.082|10.804|1.427|9.889|17.440|5.358|9.947|
|DeepACO||3.827|0.009|0.269|7.766|0.043|1.806|10.715|0.594|2.589|16.863|1.871|10.220|
|SIL||3.827|0.000|4.489|7.824|0.794|8.940|10.763|1.049|10.000|16.954|2.423|10.000|
|**LHD Frame**|**w**|**orks**||||||||||||
|FunSearch||**3.827**|**0.000**|0.909|7.780|0.225|10.212|10.803|1.423|10.084|16.897|2.080|10.095|
|ReEvo||**3.827**|**0.000**|0.763|7.777|0.191|10.095|10.857|1.925|10.044|16.891|2.040|10.167|
|EoH||**3.827**|**0.000**|1.031|7.772|0.122|10.847|10.843|1.801|10.058|16.948|2.387|10.086|
|MEoH||**3.827**|**0.000**|0.619|7.797|0.443|9.884|10.881|2.152|10.077|17.081|3.188|9.931|
|Hercules||**3.827**|**0.000**|0.823|7.776|0.169|10.970|10.827|1.651|10.101|16.873|1.935|10.684|
|DASH (Ours)||**3.827**|**0.000**|**0.044**|**7.769**|**0.086**|**1.136**|**10.677**|**0.243**|**1.940**|**16.714**|**0.974**|**3.680**|
|8<br>FunSearch|||8<br>Re|Evo|8|EoH|8|MEoH|8|Hercules|8|DASH (o|urs)|
|6<br>(%)||4|6|4|6||6<br><br>4||6<br><br>4||6<br><br>4||4<br>R|
|4<br>Gap||3|4|3|4||4<br>3||4<br>3||4<br>3||3<br>tLD|
|2||2|2|2|2||2<br>2||2<br>2||2<br>2||2|
|||1||1|||1||1||1||1|
|0<br>25<br>50<br>Evaluations|7<br>|5<br>100|0<br>25<br>5<br>Evalu|0<br>75<br>100<br>ations|0<br>25|50<br>75<br>Evaluations|100<br>0<br>2|5<br>50<br>75<br>Evaluations|100<br>0|25<br>50<br>75<br>Evaluations|100|0<br>25<br>50<br>Evaluati|75<br>100<br>ons|



Figure 3: **Evolutionary dynamics of major LHD frameworks on TSP500.** Across 5 independent runs (100 evaluations each), we report the best-so-far gap (blue, left axis) and tLDR (orange, right axis) for FunSearch, ReEvo, EoH, MEoH, Hercules, and DASH. Lines show the mean and shaded bands show the variability across runs. 

natorial optimization tasks? 

- **RQ2 (Component and Design Analysis):** How do the components and design choices of DASH contribute to solution quality and runtime efficiency? 

- **RQ3 (Generalizability and Robustness Analysis):** How well does DASH transfer across solver backbones and distribution shifts? 

- **RQ4 (Profile-Aware Retrieval Analysis):** How does profile-aware retrieval organize heterogeneous instances, and how does grouping granularity affect specialization and efficiency? 

### **5.2 Main Results (RQ1)** 

Table 2 reports the main TSP results across four scales. Overall, DASH achieves the best balance between gap and time, and its advantage becomes most evident on larger instances. We draw the following observations: 

- DASH is consistently competitive with strong conventional, neural, and prior LHD baselines. On the hardest setting TSP500, it improves the GLS backbone from 6.400% gap at 10.114 s to 0.974% gap at 3.680 s, validating the benefit of jointly optimizing mechanisms and schedules. 

- The advantage of DASH appears across scales. On TSP20 and TSP100, some LHD baselines already reach zero or near-zero gap, but further 

9 

Table 3: **Performance comparison on CVRP/VRPTW/MKP.** We report two metrics: Gap (%) and Time (s). CVRP 100 and CVRP 500 denote CVRP instances with 100 and 500 customers and use a 5 s runtime budget. VRPTW 15 and VRPTW 20 denote VRPTW instances with 15 and 20 customers and use a 60 s runtime budget. MKP 10 and MKP 30 denote MKP instances with 500 items and 10 and 30 constraints and use a 5 s runtime budget. Bold and underlined values indicate the best and second-best LHD results. 

|Method|CVRP|100|CVR|P 500|VRPT|W 15|VRPT|W 20|MK|P 10|MK|P 30|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|Gap (%)|Time (s)|Gap (%)|Time (s)|Gap (%)|Time (s)|Gap (%)|Time (s)|
|FunSearch|0.592|5.043|6.487|5.084|2.437|47.538|5.684|53.417|**0.964**|5.083|**1.861**|5.106|
|EoH|0.458|5.021|**3.742**|5.086|4.126|56.241|7.836|58.274|1.781|5.012|2.736|5.018|
|ReEvo|0.447|5.036|5.286|5.093|2.781|59.826|5.143|54.612|1.327|4.742|2.214|4.893|
|MEoH|0.682|5.017|6.018|5.074|**1.918**|60.127|**4.638**|60.356|1.546|4.618|2.438|4.781|
|Hercules|0.431|5.074|5.167|5.081|3.347|60.642|6.913|60.781|2.084|5.241|3.147|5.318|
|DASH (Ours)|**0.334**|**2.013**|3.935|**3.442**|2.084|**18.731**|4.927|**22.614**|1.083|**2.684**|1.978|**2.941**|



- evolution does not reduce the final gap and can even increase runtime, especially on TSP20. In contrast, DASH can still reduce runtime while preserving the same final gap, showing that runtime schedule can improve efficiency even when solution quality is already near-optimal. 

- Compared with prior endpoint-driven LHD baselines such as EoH, DASH achieves lower runtime together with lower final gap on larger instances. On TSP500, DASH reaches a 0.974% gap in 3.680 s, whereas the compared baselines remain close to the full budget and still produce gaps around 2% or higher, which is consistent with the effect of trajectory-aware selection and runtime schedule optimization in DASH. 

- Compared with the efficiency-aware LHD baseline MEoH, DASH maintains better gap while preserving a runtime advantage on larger instances. MEoH reduces runtime more efficiently on smaller instances, but on TSP500 its final gap remains clearly higher than that of DASH. This shows that runtime reduction alone does not lead to better overall performance on larger instances. 

Table 3 further validates the effectiveness of DASH on other combinatorial optimization tasks. We consider two related routing tasks, CVRP and VRPTW, and extend the evaluation to a different resource-allocation task, MKP. To ensure a fair comparison, we use ACO as the shared backbone and keep the editable solver scope the same for all LHD baselines, while DASH additionally optimizes the runtime schedule. For CVRP, which extends TSP with capacity constraints, DASH achieves the lowest gap on CVRP100 while reducing runtime. On CVRP500, it remains close to the stronger baselines in gap while reducing runtime from about 5 s to 3.442 s. VRPTW increases the difficulty by introducing time-window 

constraints, and we accordingly use a larger runtime budget. Under this setting, DASH reduces runtime while keeping the final gap in a comparable range. We further extend the evaluation to MKP. On both MKP10 and MKP30, DASH reduces runtime from about 5 s to around 3 s while keeping the final gap close to the stronger baselines. 

Figure 3 visualizes the evolutionary dynamics on TSP500 across repeated runs. FunSearch, ReEvo, EoH, and Hercules all reduce the best-so-far gap over evaluations, but their tLDR curves remain lower and increase more gradually. MEoH also raises tLDR more quickly, but its gap curve flattens earlier. Since DASH uses tLDR as the trajectoryaware selection signal, the retained solvers show both faster tLDR growth and stronger best-so-far gap reduction over evaluations. 

### **5.3 Component and Design Analysis (RQ2)** 

We use TSP100 and CVRP100 as representative tasks for component and design analysis. Table 4 validates the contribution of DASH’s components. Removing SSL-1 causes the largest slowdown on both tasks, indicating that most runtime reduction comes from schedule compression. Removing tLDR from selection degrades both runtime and solution quality, consistent with its role in favoring solvers with efficient early convergence. In contrast, removing SSL-2 mainly degrades the final gap with only minor runtime changes, matching its role as a quality-oriented enhancement stage. Finally, disabling PLR worsens both gap and time, showing that profile-based retrieval improves group-specific solver selection at inference. 

Table 5 further separates the roles of the three iteration layers. Removing MDL causes the largest gap degradation, indicating that mechanism discovery is the main source of the gap reduction. 

10 

Table 4: **Ablation study on DASH components.** We report Gap (%) and Time (s) on TSP100 and CVRP100. 

|Variant|TSP|100|CVRP|100|
|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|
|**DASH (Full)**|**0.086**|**1.136**|**0.334**|**2.013**|
|w/o tLDR|0.452|2.200|0.385|4.859|
|w/o SSL-1|0.105|8.505|0.362|6.201|
|w/o SSL-2|0.165|1.002|0.392|1.920|
|w/o PLR|0.155|1.980|0.450|2.963|



Removing MCL mainly increases runtime while only moderately affecting gap, which is consistent with MCL pruning redundant branches without materially changing the schedule. Removing SSL almost eliminates the efficiency advantage of DASH, showing that runtime schedule optimization is the primary driver of runtime reduction. 

Table 5: **Ablation study on DASH iteration layers.** We report Gap (%) and Time (s) on TSP100 and CVRP100. 

|Variant|TSP|100|CVRP|100|
|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|
|**DASH (Full)**|**0.086**|**1.136**|**0.334**|**2.013**|
|w/o MDL|0.625|0.950|0.812|1.845|
|w/o MCL|0.114|1.680|0.358|2.550|
|w/o SSL (Full)|0.158|9.105|0.380|8.950|



We also examine how the trajectory metric used in selection affects the resulting gap and runtime. Concretely, we replace tLDR with an alternative metric while keeping the rest of DASH unchanged. We compare tLDR against three alternatives: **Terminal Time** , which uses runtime _t_ run as the efficiency signal; **Time-to-10%** , the time required to reach 0 _._ 1 _·_ Gap(0) on the incumbent trajectory, capped at _T_ if the threshold is not reached; and **Linear AUC** , the normalized linear-space area under the best-so-far gap curve, _T_<sup><u>1</u></sup> �0 _T_<sup>Gapbest(</sup><sup>_τ_)</sup><sup>_dτ_.</sup> Replacing tLDR with alternative metrics changes the gap and time trade-off in different ways. Using _Terminal Time_ yields the lowest runtime but also the worst gap on both tasks, indicating that a purely runtime-oriented signal tends to select solvers with weaker refinement. _Time-to-10%_ and _Linear AUC_ recover part of this loss, but both remain inferior to tLDR. _Time-to-10%_ captures whether a solver reaches an early target quickly, but it does not distinguish candidates well after the threshold is reached. _Linear AUC_ uses the full trajectory, but in linear space it is less sensitive to later-stage improvements when the gap is al- 

Table 6: **Sensitivity to selection design.** We study two design choices in DASH: the trajectory metric used in selection and the shared comparison margin _ϵ_ . Results are reported on TSP 100 and CVRP 100. 

|Variant|TSP|100|CVRP|100|
|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|
|**Trajectory Met**|**ric for Sele**|**ction**|||
|DASH (tLDR)|**0.086**|1.136|**0.334**|2.013|
|Terminal Time|0.585|**0.850**|0.852|**1.420**|
|Time-to-10%|0.242|1.020|0.425|1.880|
|Linear AUC|0.130|1.105|0.468|1.950|
|**Comparison M**|**argin**||||
|_ϵ_= 0_._01|0.118|**1.028**|0.368|**1.926**|
|_ϵ_= 0_._05|**0.086**|1.136|**0.334**|2.013|
|_ϵ_= 0_._10|0.147|1.284|0.401|2.467|



ready small. In contrast, tLDR achieves the best gap with only moderate runtime increase, which is consistent with using the full convergence trajectory in log-space as the selection signal rather than relying only on runtime, a single threshold, or a linear-space summary. 

Table 6 further examines how the trade-off between gap and runtime changes with the shared comparison margin _ϵ_ . In our experiments, _ϵ_ = 0 _._ 01 makes acceptance more aggressive and slightly lowers runtime, but leads to worse final gap on both tasks, while _ϵ_ = 0 _._ 10 yields more conservative selection and tends to reject moderate but still useful improvements, resulting in a weaker balance between gap and runtime. We therefore use _ϵ_ = 0 _._ 05 as a practical default in the experiments. 

Table 7: **Transferability of DASH across solver frameworks on TSPLIB.** We report Gap (%) and Time (s) on small (14–200) and large (201–1000) instances. 

|Method|TSPLI|B-small|TSPLIB|-large|
|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|
|GLS|1.263|1.605|4.581|32.597|
|ILS|1.209|2.231|3.969|38.212|
|LKH|0.957|3.777|3.718|33.001|
|DASH+GLS|0.122|0.263|1.224|4.520|
|DASH+ILS|0.102|0.276|1.157|5.300|
|DASH+LKH|0.092|0.315|1.070|4.297|



### **5.4 Generalizability and Robustness Analysis (RQ3)** 

Besides validating DASH across different tasks, we also examine whether its evolutionary optimization transfers across different solver backbones within the same task. Table 7 shows that DASH consistently improves all three TSP backbones (GLS/IL- 

11 

S/LKH) on TSPLIB, reducing both gap and runtime on small and large instances. The gains across distinct backbones indicate that DASH acts as a general optimizer rather than being tied to a specific solver. 

Table 8: **Generalization Cost on TSPLIB (14–1000) with 100 evaluations.** (+Iters) increases the evaluation to 5 _×_ (500 evaluations); (+Groups) applies the same instance grouping protocol as DASH. 

|**Method**|**Evolu**|**tion**|**Te**|**st**|**Tokens (k)**|
|---|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|Input/Output|
|MEoH|2.070|20.027|3.174|14.422|44.7/27.3|
|MEoH (+Iters)|1.891|21.143|2.923|14.146|229.5/131.0|
|MEoH (+Groups)|1.660|20.521|1.690|12.967|472.9/280.6|
|Hercules|1.354|20.283|0.867|7.789|143.4/31.2|
|Hercules (+Iters)|1.125|19.990|0.822|7.990|711.4/155.7|
|Hercules (+Groups)|0.792|18.231|0.480|7.142|1401.1/322.3|
|DASH|**0.516**|**4.340**|**0.532**|**1.846**|**115.0/58.8**|



Table 8 studies generalization under a distribution shift by evaluating solvers evolved under the same 100-evaluation setting on TSPLIB. For baselines, (+Iters) increases the evolution budget to 5 _×_ , and (+Groups) trains group-specific solvers using the same grouping protocol as DASH. Among the compared baselines, MEoH uses the fewest tokens in the standard setting, but its gap increases clearly from evolution to TSPLIB. Increasing the evaluation budget or introducing group-specific training can reduce this shift, but both require substantially higher token cost. Compared with MEoH, Hercules is more stable under the same shift, which is consistent with its use of historical search experience during heuristic generation and evaluation. In contrast, DASH maintains low gap from evolution to TSPLIB test while also achieving the lowest runtime on both sides, showing that PLR improves robustness to distribution shift without the additional optimization cost. 

Table 9 compares Conventional Solvers and LHD Frameworks under time-constrained evaluation, where the time budget is fixed to 10 s for TSPLIB-small and 60 s for TSPLIB-large. Under the same budget, DASH achieves the best results among the compared LHD frameworks on both instance scales. On TSPLIB-small, DASH surpasses best-performing LHD framework Hercules, reducing the gap from 0.216% to 0.122% and the runtime from 0.576 s to 0.263 s. On TSPLIB-large, DASH again achieves both lower gap and lower runtime, improving from 1.967% to 1.224% in gap and from 19.977 s to 4.520 s in runtime. DASH is 

Table 9: **TSPLIB performance under time-constraint evaluation.** We fix the time budget across all methods, set _T_ =10s for TSPLIB-small (14–200) and _T_ =60s for TSPLIB-large (201–1000). 

|Method|TSPLI|B-small|TSPLIB|-large|
|---|---|---|---|---|
||Gap (%)|Time (s)|Gap (%)|Time (s)|
|**Convention**|**al Solver**||||
|Concorde|0.000|0.332|0.000|11.797|
|LKH3|0.000|0.211|0.000|2.789|
|OR-Tools|1.291|7.310|3.586|60.000|
|**LHD Frame**|**works**||||
|FunSearch|1.163|1.048|2.760|12.898|
|ReEvo|1.396|2.503|3.189|36.996|
|EoH|3.162|1.574|4.021|24.225|
|MEoH|3.042|1.079|3.397|36.968|
|Hercules|0.216|0.576|1.967|19.977|
|DASH|0.122|0.263|1.224|4.520|



Table 10: **TSPLIB results under time-unconstrained evaluation.** We report Gap (%) and Time (s) on TSPLIB-small (14–200) and TSPLIB-large (201–1000). For DASH, SSL is disabled during evaluation. 

|Method<br>TSPLI|B-small|TSPLIB|-large|
|---|---|---|---|
|Gap (%)|Time (s)|Gap (%)|Time (s)|
|**Conventional Solver**||||
|Concorde<br>0.000|0.273|0.000|10.285|
|LKH3<br>0.000|0.150|0.001|5.118|
|OR-Tools<br>2.650|0.452|4.206|15.619|
|**LHD Frameworks**||||
|FunSearch<br>1.160|1.739|2.607|16.820|
|ReEvo<br>1.411|2.668|1.443|125.306|
|EoH<br>3.132|0.970|4.022|26.714|
|MEoH<br>3.035|1.066|3.397|23.657|
|Hercules<br>0.096|0.708|1.742|20.609|
|DASH w/o SSL<br>0.010|2.104|0.824|26.240|



also the LHD method closest to the C implementation LKH3, especially on TSPLIB-small where it reaches near-zero gap with comparable runtime. 

Table 10 further compares Conventional Solvers and LHD Frameworks under time-unconstrained evaluation. We remove the time budget and, for LHD frameworks, fix the GLS backbone to 1000 iterations. For a fair comparison, we disable SSL in DASH. Under this setting, most LHD frameworks improve further, especially on TSPLIBlarge. ReEvo provides a representative example: its gap on TSPLIB-large improves from 3.189% to 1.443%, but its runtime increases from 36.996 s to 125.306 s. Under the same unconstrained setting, DASH w/o SSL reaches 0.824% on TSPLIB-large in 26.240 s, and 0.010% on TSPLIB-small in 2.104 s. Although SSL is disabled in this setting, these results still show that the mechanisms evolved by DASH retain clear potential for further improve- 

12 



<!-- Start of picture text -->
GPT-5.4 DeepSeek-V3.2 Gemini-3.1-Pro Claude-4.6-Sonnet Qwen3.5-35B-A3B<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>10.0<br>7.5<br>5.0<br>2.5<br>FunSearch ReEvo EoH MEoH Hercules DASH<br>FunSearch ReEvo EoH MEoHHercules DASH FunSearch ReEvo EoH MEoHHercules DASH FunSearch ReEvo EoH MEoHHercules DASH FunSearch ReEvo EoH MEoHHercules DASH FunSearch ReEvo EoH MEoHHercules DASH<br>Gap (%)<br>Time (s)<br><!-- End of picture text -->

Figure 4: **Base-model sensitivity on TSP 100.** Using five base LLMs for solver generation (5 runs, 100 evaluations each), we report the final best-so-far gap (top) and the runtime of that best solver (bottom). 

ment when additional solving budget is allowed. 

Figure 4 evaluates sensitivity to the underlying code-generation model. Changing the base LLM does affect the absolute performance of all methods: the overall gaps are lower under GPT-5.4 (OpenAI, 2026), Gemini-3.1-Pro (DeepMind, 2026), and Claude-4.6-Sonnet (Anthropic, 2026), and become larger under DeepSeek-V3.2 (DeepSeek-AI, 2025) and Qwen3.5-35B-A3B (Team, 2025). Nevertheless, DASH remains consistently strong across all five models, maintaining the lowest or nearlowest gap together with a clear runtime advantage. This shows that the advantage of DASH is not tied to a single base model. 

### **5.5 Profile-Aware Retrieval Analysis (RQ4)** 

The TSPLIB transfer results already show that PLR reduces the need to restart adaptation under shifted instance distributions. To support this behavior, DASH constructs a lightweight profile vector for each instance, standardizes these features, and clusters them into _G_ groups. The resulting groups are used both for stratified evolution and for test-time retrieval through the nearest group prototype. 

To illustrate the profile structure, we characterize the features of 100 TSP instances and 100 CVRP instances. For TSP, the profiles include scale, distance statistics, local density, and shape descriptors. For CVRP, the profiles include instance scale, geometric density, depot-relative structure, demand variation, and load pressure. Figure 5 shows that the resulting groups separate both TSP and CVRP instances along interpretable profile dimensions rather than simply partitioning by size. 

Table 11 further studies the sensitivity to the number of instance groups _G_ . Increasing _G_ be- 

yond 10 yields marginal gap improvements on both tasks, while evaluation cost rises because the same total evolution budget must be spread across more groups. We therefore use _G_ =10 as the default trade-off between specialization and evaluation efficiency. 

## **6 Conclusion** 

We revisit LLM-Driven Heuristic Design from a dynamics perspective, evaluating solvers by their convergence trajectories rather than only terminal gap. We introduce the Trajectory-aware Lyapunov Decay Rate (tLDR), a metric computed from execution traces that captures the rate and consistency of convergence throughout the run. Guided by tLDR, DASH co-evolves search mechanisms and runtime schedules through three iteration layers: MDL, MCL, and SSL under a unified acceptance protocol, so that solver generation is driven not only by final quality but also by how efficiently useful progress is produced over time. The ablation results further show that these components play different and complementary roles: MDL mainly improves the quality of discovered mechanisms, MCL reduces redundant exploration, and SSL converts those stronger candidates into shorter realized runtimes. 

To reduce re-adaptation under heterogeneous instance groups, DASH incorporates Profiled Library Retrieval (PLR), which decouples group-specific archiving from global evolution to enable profileaware warm starts. This makes it possible to harvest specialized solvers during the evolutionary pro- 

cess instead of restarting adaptation from scratch whenever the instance distribution shifts. Across four combinatorial optimization problems, DASH 

13 



<!-- Start of picture text -->
3 TSP: PCA of standardized profiles TSP: scale-density view CVRP: PCA of standardized profiles CVRP: load-density view<br>3.5<br>2 4.0 3<br>1 3.0<br>3.5 2<br>0<br>2.5<br>1 3.0 1<br>2 0 2.0<br>2.5<br>3<br>1 1.5<br>4<br>2.0<br>3 2 1 0 1 2 3 4 4.0 4.5 5.0 5.5 6.0 6.5 7.0 3 2 1 0 1 2 3 4 1 2 3 4 5<br>PC1 Scale PC1 Load Pressure<br>PC2 PC2<br>Density Density<br><!-- End of picture text -->

Figure 5: **Instance profiling and grouping for TSP and CVRP.** We visualize standardized profile vectors for 100 TSP instances and 100 CVRP instances, and apply k-means with _G_ =10. _(a)_ PCA projection of TSP profiles, colored by group assignment. _(b)_ TSP scale–density view using the scale feature log( _n_ ) and a nearest-neighbor based density proxy. _(c)_ PCA projection of CVRP profiles, colored by group assignment. _(d)_ CVRP load–density view using log(<sup>�</sup> _i_<sup>_di/Q_) and a geometric density proxy.</sup> 

Table 11: **Sensitivity to the number of instance groups** _G_ **on TSP and CVRP.** We vary the grouping granularity _G ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ under the same evolution budget (100 evaluations). We report evolution/test gap and runtime, together with evaluation cost per iteration ( _Eval./iter._ ) and total evaluation cost ( _Total Eval._ ). 

|_G_|**Evo. G **|**ap (%)**|**Evo. T **|**ime (s)**|**Test G**|**ap (%)**|**Test T**|**ime (s)**|**Eval.**|**/iter. (s)**|**Total E**|**val. (min)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**TSP**|**CVRP**|**TSP**|**CVRP**|**TSP**|**CVRP**|**TSP**|**CVRP**|**TSP**|**CVRP**|**TSP**|**CVRP**|
|5|0.550|0.416|2.050|2.325|0.620|0.469|1.950|1.911|28.1|31.9|46.7|53.0|
|10|0.419|0.317|1.905|2.160|0.442|0.334|1.775|2.013|35.0|39.7|58.3|66.1|
|15|0.410|0.310|1.915|2.172|0.438|0.331|1.780|2.019|50.5|57.3|83.3|94.5|
|20|0.408|0.308|1.925|2.183|0.437|0.330|1.785|2.024|65.7|74.5|108.3|122.8|



improves runtime efficiency by over 4 _×_ while achieving a better balance between gap and runtime than prior LHD baselines. It also generalizes across multiple solver backbones and maintains performance under distribution shift with substantially lower adaptation cost. 

14 

## **References** 

- Emile Aarts and Jan Karel Lenstra. 2018. _Local Search in Combinatorial Optimization_ . Princeton University Press. 

Anthropic. 2026. Claude sonnet 4.6 system card. 

- Florian Arnold and Kenneth Sörensen. 2019. Knowledge-guided local search for the vehicle routing problem. _Computers & Operations Research_ , 105:32–46. 

- John E. Beasley. 1990. OR-Library: Distributing test problems by electronic mail. _Journal of the Operational Research Society_ , 41(11):1069–1072. 

- Edmund K. Burke, Michel Gendreau, Matthew Hyde, Graham Kendall, Gabriela Ochoa, Ender Özcan, and Rong Qu. 2013. Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ , 64(12):1695–1724. 

- William J. Cook, David L. Applegate, Robert E. Bixby, and Vašek Chvátal. 2011. _The Traveling Salesman Problem: A Computational Study_ . Princeton University Press. 

- Pham Vu Tuan Dat, Long Doan, and Huynh Thi Thanh Binh. 2025. Hsevo: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _AAAI_ , pages 26931– 26938, Philadelphia, PA, USA. 

- Google DeepMind. 2026. Gemini 3.1 pro model card. Technical report. 

- DeepSeek-AI. 2025. Deepseek-v3.2: Pushing the frontier of open large language models. _CoRR_ , abs/2512.02556. 

- Marco Dorigo, Mauro Birattari, and Thomas Stützle. 2006. _Ant Colony Optimization_ , volume 1. 

- Michael R. Garey and David S. Johnson. 1983. _Computers and Intractability: A Guide to the Theory of NP-Completeness_ . W. H. Freeman. 

- Shuhan Guo, Nan Yin, James Kwok, and Quanming Yao. 2025. Nested-refinement metamorphosis: Reflective evolution for efficient optimization of networking problems. In _Findings of ACL_ , pages 17398–17429, Vienna, Austria. 

- Eric A. Hansen and Shlomo Zilberstein. 1996. Monitoring the progress of anytime problem-solving. In _AAAI_ , pages 1229–1234, Portland, Oregon, USA. 

- Keld Helsgaun. LKH-3: Lin–kernighan–helsgaun TSP solver. http://webhotel4.ruc.dk/~keld/ research/LKH-3/. 

- Keld Helsgaun. 2000. An effective implementation of the lin-kernighan traveling salesman heuristic. _European Journal of Operational Research_ , 126(1):106– 130. 

- Hassan K Khalil and Jessy W Grizzle. 2002. _Nonlinear systems_ , volume 3. Prentice hall Upper Saddle River, NJ. 

- Minsu Kim, Junyoung Park, and Jinkyoo Park. 2022. Sym-nco: Leveraging symmetricity for neural combinatorial optimization. In _NeurIPS_ , New Orleans, LA, USA. 

- Wouter Kool, Herke van Hoof, and Max Welling. 2019. Attention, learn to solve routing problems! In _ICLR_ , New Orleans, LA, USA. 

- Bernhard Korte and Jens Vygen. 2008. _Combinatorial Optimization: Theory and Algorithms_ . Springer. 

- Yeong-Dae Kwon, Jinho Choo, Byoungjip Kim, Iljoo Yoon, Youngjune Gwon, and Seungjai Min. 2020. POMO: policy optimization with multiple optima for reinforcement learning. In _NeurIPS_ , Virtual Event. 

- Jing Li, Yin David Yang, and Nikos Mamoulis. 2013. Optimal route queries with arbitrary order constraints. _IEEE Transactions on Knowledge and Data Engineering_ , 25(5):1097–1110. 

- Marius Lindauer, Holger H. Hoos, Frank Hutter, and Torsten Schaub. 2015. Autofolio: An automatically configured algorithm selector. _Journal of Artificial Intelligence Research_ , 53:745–778. 

- Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _ICML_ , pages 32201–32223, Vienna, Austria. 

- Helena R. Lourenço, Olivier C. Martin, and Thomas Stützle. 2003. _Iterated Local Search_ . Springer. 

- Fu Luo, Xi Lin, Yaoxin Wu, Zhenkun Wang, Xialiang Tong, Mingxuan Yuan, and Qingfu Zhang. 2025. Boosting neural combinatorial optimization for largescale vehicle routing problems. In _ICLR_ , Singapore. 

OpenAI. 2026. Introducing GPT-5.4. Technical report. 

- Laurent Perron and Vincent Furnon. Or-tools. https: //developers.google.com/optimization/. 

- John R. Rice. 1976. The algorithm selection problem. In _Advances in Computers_ , volume 15, pages 65–118. Elsevier. 

- Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995):468–475. 

- Marius M. Solomon. 1987. Algorithms for the vehicle routing and scheduling problems with time window constraints. _Operations Research_ , 35(2):254–265. 

15 

- Qwen Team. 2025. Qwen3 technical report. _CoRR_ , abs/2505.09388. 

- Yongxin Tong, Dingyuan Shi, Yi Xu, Weifeng Lv, Zhiwei Qin, and Xiaocheng Tang. 2023. Combinatorial optimization meets reinforcement learning: Effective taxi order dispatching at large-scale. _IEEE Transactions on Knowledge and Data Engineering_ , 35(10):9812–9823. 

- Eduardo Uchoa, Diego Pecin, Artur Alves Pessoa, Marcus Poggi, Thibaut Vidal, and Anand Subramanian. 2017. New benchmark instances for the capacitated vehicle routing problem. _European Journal of Operational Research_ , 257(3):845–858. 

- Christos Voudouris and Edward P. K. Tsang. 1999. Guided local search and its application to the traveling salesman problem. _European Journal of Operational Research_ , 113(2):469–499. 

   - Zhongyun Zhang, Lei Yang, Jiajun Yao, Chao Ma, and Jianguo Wang. 2024. Joint optimization of pricing, dispatching and repositioning in ride-hailing with multiple models interplayed reinforcement learning. _IEEE Transactions on Knowledge and Data Engineering_ , 36(12):8593–8606. 

   - Zhi Zheng, Zhuoliang Xie, Zhenkun Wang, and Bryan Hooi. 2025. Monte carlo tree search for comprehensive exploration in LLM-based automatic heuristic design. In _ICML_ , Vancouver, BC, Canada. 

   - Jianan Zhou, Yaoxin Wu, Zhiguang Cao, Wen Song, Jie Zhang, and Zhenghua Chen. 2023. Learning large neighborhood search for vehicle routing in airport ground handling. _IEEE Transactions on Knowledge and Data Engineering_ , 35(9):9769–9782. 

   - Shlomo Zilberstein. 1996. Using anytime algorithms in intelligent systems. _AI Magazine_ , 17(3):73–73. 

- David H. Wolpert and William G. Macready. 1997. No free lunch theorems for optimization. _IEEE Transactions on Evolutionary Computation_ , 1(1):67–82. 

- Xuan Wu, Di Wang, Chunguo Wu, Lijie Wen, Chunyan Miao, Yubin Xiao, and You Zhou. 2025. Efficient heuristics generation for solving combinatorial optimization problems using large language models. In _KDD_ , pages 3228–3239, Toronto, ON, Canada. 

- Shunyu Yao, Fei Liu, Xi Lin, Zhichao Lu, Zhenkun Wang, and Qingfu Zhang. 2025. Multi-objective evolution of heuristic using large language model. In _AAAI_ , pages 27144–27152, Philadelphia, PA, USA. 

- Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. In _NeurIPS_ , Vancouver, BC, Canada. 

- Haoran Ye, Jiarui Wang, Zhiguang Cao, Helan Liang, and Yong Li. 2023. DeepACO: Neural-enhanced ant systems for combinatorial optimization. In _NeurIPS_ , New Orleans, LA, USA. 

- Jing Yuan, Yu Zheng, Xing Xie, and Guangzhong Sun. 2013a. T-drive: Enhancing driving directions with taxi drivers’ intelligence. _IEEE Transactions on Knowledge and Data Engineering_ , 25(1):220–232. 

- Nicholas Jing Yuan, Yu Zheng, Liuhang Zhang, and Xing Xie. 2013b. T-finder: A recommender system for finding passengers and vacant taxis. _IEEE Transactions on Knowledge and Data Engineering_ , 25(10):2390–2403. 

- Zhiqin Zhang, Jingfeng Yang, Zhiguang Cao, and Hoong Chuin Lau. 2025. Neuro-ins: A learningbased one-shot node insertion for dynamic routing problems. _IEEE Transactions on Knowledge and Data Engineering_ , 37(9):5495–5507. 

16 

