# eoopt 最终目标设计与开发路线图

## Context（为什么做这件事）

三期路线前两期已完成并验证（最简验证 MVP + 工程最小 MVP + ADR-0008 控制变量实验），**第三期阶段 1（双后端内核）亦已完成**；内核（`manifold/`/`continuation/`/`core/`）稳定，两级 seam 架构已被两阶段实测兑现——"换期只加 adapter、不改内核"已成立（当前 59 测试全绿）。

现在要为**最终目标**（三期）给出明确的**目标设计 + 开发路线图**，整合用户三条设想 + lit-review 调研 + 原始批准方案明列的全部最终目标项。最终目标定调如下：

> **最终目标**：把 eoopt 做成一个**双表述体系原生兼容**（电子光学 + 加速器）的匹配流形优化平台——内核（流形投影 + 切向优化 + atlas 延拓）领域无关，两套物理表述作为对等后端插入；内置常用高阶匹配方法（C1-C3 平衡、twiss 阈值/指定点匹配、色品匹配），允许用户自定义匹配函数；支持**不等式裁剪**把 M 切成孤岛、**可插拔外部求解器/仿真**、**鲁棒 CVaR 目标**、**样本学习流形**等扩展；以**流形内四族切向优化器（DFO / ES / GA / BO）**覆盖高维含噪 / 病态各向异性 / 组合多模 / 极贵少样本场景；以**采样-吸引-聚类**快速判定多分支结构，以**atlas 延拓 + 切向优化**精覆盖每支、以**CI-NEB/鞍点**判定分支间连通性；最终支持**多目标 Pareto 延拓**。

本文件是**目标设计 + 路线图**，不是实现计划。实现粒度与测试算例留到各阶段开工时定（用户明确）。

---

## 一、最终目标架构设计

### 1.1 总体分层（内核不变，扩物理层、匹配编译层与若干扩展 seam）

```
physics/{eo, accel}          ← §1.2 双后端，领域特定
  → constraints/specs/        ← §1.3 MatchingSpec 编译器（含不等式裁剪、样本学习流形）
  → objective/                ← §1.4 领域目标 adapter（含鲁棒 CVaR）
manifold/                     ← 内核（不动）：project / tangent / spectrum
continuation/                 ← 内核（扩多分支）：atlas + 分支枚举/连通
optimize/                     ← 内核（扩四族 + 可插拔求解器）：RiemannTR / PatternSearch / NM / DFO / ES / GA / BO / 外部
experiments/branch_probe/     ← §1.6 采样-吸引-聚类多分支判定
core/                         ← 叶子（不动）
```

依赖方向：`physics → {constraints/specs, objective} → manifold → {continuation, optimize} → experiments`。内核零改动。

### 1.2 物理层：双后端（对应原方案 tier-3 "可插拔任意求解器/仿真"的物理侧）

把 [physics/base.py](src/eoopt/physics/base.py) 的 `PhysicsModel`（硬绑 EO 的 R/Cs）提升为领域无关 `PhysicsBackend`，下挂两个对等后端：

- **`ElectronOpticsBackend`**：`transfer_matrix`(2×2 R)、`spherical_aberration`(C_s)、`chromatic_aberration`(C_c)、像差系数 `c1/c3/c5`（probe-ray 已算，[gpt_proberay.py](src/eoopt/physics/gpt_proberay.py)）。实现：现有 `BzGaussStack`（傍轴 ODE + 像差 ODE）。
- **`AcceleratorBackend`**：`ring_matrix`(一圈传输矩阵 6×6 或分平面 2×2)、`twiss`(β/α/μ 沿 s)、`chromaticity`(ξ₁,ξ₂)、`dispersion`(η/η')。实现：**自研**——类 `BzGaussStack` 走元件矩阵连乘（漂移/四极/弯曲的 6D 线性映射），全可微、复步 Jacobian 可用、与 EO 后端对称。`dynamic_aperture` 为可选黑箱接口（DA 工具/粒子追踪），不进一阶后端。
- **高阶物理扩展**（原方案 tier-3 物理项，作为后端的可选能力，路线图后期）：differential-algebra 高阶映射、厚透镜内部截面 Φ(z_b,z_a)、浸没靶、外部 3D 场图。这些是 `PhysicsBackend` 的可选方法，不影响一阶匹配流形主链路。
- 每个后端有唯一 q→物理映射（复用 `unpack_lenses` 模式），保证约束与目标同一套物理。

### 1.3 匹配编译层：MatchingSpec（新层 `constraints/specs/`）

"匹配什么"与"怎么算残差"分离。`MatchingSpec` 是用户可组合规格，编译器翻译成 `ConstraintModel`（复用 `ConstraintBase` 复步 Jacobian，[constraints/base.py:76](src/eoopt/constraints/base.py#L76)）：

- **EO 内置 spec**：`ImagingSpec`(B=0)、`MagnificationSpec`(A=M)、`AfocalSpec`、`TelescopicSpec`、`AberrationBalanceSpec`(C1-C3 平衡——落地 HANDOVER §7.3 悬置的离焦平衡选型)。
- **加速器内置 spec**：`TwissThresholdSpec`(β/α/μ 在指定点 ≤ 阈值或 = 指定值)、`TwissMatchSpec`(指定点 twiss = 目标)、`ChromaticitySpec`(ξ₁,ξ₂ = 目标)、`DispersionSpec`、`PeriodicSpec`(一圈 twiss 闭合)。
- **用户自定义**：`FunctionalSpec(residual_fn)`——用户给 `q→c(q)`，自动拿复步 Jacobian。**这是"允许用户自行实现匹配计算函数"的直接落点**。
- **不等式裁剪** `InequalitySpec(g(q)≤0)`（原方案 tier-3 明列）：把 `g(q)≤0` 作为"软裁剪"加入约束体系——流形 `c(q)=0` 被不等式切成多个孤岛，atlas 延拓在触碰 `g=0` 边界时停止/分叉。这天然与 §1.6 多分支层协同（孤岛=分支）。当前只有盒式 `bounds`（[continuation/chart.py:39](src/eoopt/continuation/chart.py#L39)），需扩展为一般 `g(q)≤0`。
- **样本学习流形** `SampleLearnedConstraint`（原方案 tier-3 明列）：用 AE/diffusion 学一个隐式约束 `c_learned(q)=0`（如从历史可行设计学"经验可行域"），插入同一 `ConstraintModel` seam。属较前沿，路线图后期。
- **组合**：`c = [spec1(q); spec2(q); ...]`，r = 总等式约束数，d = n−r 自动确定；不等式 spec 单独管理为裁剪集。

### 1.4 目标层：双表述目标 + 鲁棒 CVaR（对应原方案 tier-3 "鲁棒 E[J]+λ·CVaR_α"）

`Objective` 接口不变（`value→float` + `noise_scale`），新增领域 adapter 与鲁棒包装：

- EO：`SpotObjective`(已有)、`AberrationObjective`(有符号 C_s/C_c 平衡，transfer §四"必须自造件#1")、`ThroughputObjective`。
- 加速器：`EmittanceObjective`、`DynamicApertureObjective`(黑箱/代理)、`ChromaticityMarginObjective`。
- **鲁棒目标** `RobustObjective(objective, alpha, lam)`（原方案 tier-3 明列）：包装一个含噪 `Objective`，返回 `E[J] + λ·CVaR_α(J)`——用 CRN 样本估计均值与 CVaR，`noise_scale` 已有可复用。落在目标 seam，不动内核。属中后期。
- 多目标/Pareto 为路线图后期（§三 阶段 8）。

### 1.5 切向优化器层：多条并列 adapter + 可插拔外部求解器（对应原方案 tier-3 "可插拔任意求解器"的求解器侧）

`InManifoldOptimizer`（[optimize/base.py](src/eoopt/optimize/base.py)）下并列 adapter，用户按问题特性选：

| adapter | 梯度 | 含噪 | 适用 | 来源 |
|---|---|---|---|---|
| `RiemannianTR` | 需解析梯度 | 否 | 确定性 EO、低维 | 已有 |
| `ProjectedPatternSearch` | 无 | 是 | GPT 含噪、低维 | 已有 |
| `ManifoldNelderMead` | 无 | 是 | 补充实验 | 已有 |
| **`ManifoldDFO`** | 无 | 是 | **高维含噪低预算**（retraction 型 direct search 系，主力工作马） | **新增**（阶段 3·家族①） |
| **`ManifoldES`** | 无 | 是 | **病态各向异性 / 多模连续景观**（切空间 CMA-ES/ManES，主攻押注） | **新增**（阶段 3·家族②） |
| **`ManifoldGA`** | 无 | 是 | **组合/离散/混合整数 + 重组式多模全局**（⚠ 蓝本待补充调研） | **新增**（阶段 3·家族③） |
| **`ManifoldBO`** | 无（可代理） | 是 | **评价极贵·低有效维/局部子问题**（可选、最低优先级） | **新增**（阶段 3·家族④） |
| **`ExternalOptimizer`** | 视外部 | 视外部 | 接 scipy/NLopt/pygmo 等 | **新增**（阶段 5） |

- **阶段 3 四族切向优化器**（`references/algorithm` 调研已落定选型、每族含多个待开发备选，详见 §三阶段 3）——两条设计不变量：**① 可移植性门**：eoopt 隐式 `c(q)=0` 流形只收 **retraction 型**（切步 + `manifold.project`）或**点云型**方法，闭式 geodesic/exp/Laplace–Beltrami 特征对/齐性空间"运动律"型排除（桥 [absil2012]：`project`＝合法 retraction）；**② 几何各向异性由确定性侧"算"**（`spectrum.py` 的 `J_c` SVD + 一阶段 whiten，κ≈20），四族只追 whiten 后残差：
  - `ManifoldDFO`（家族①，主力工作马）：切空间（ker J_c）无梯度直接搜索 / 模型型 DFO，每步 `project` 重牵引、读 `noise_scale` 调步长。备选：确定性 poll 直接搜索 [kungurtsev2024] / 概率下降随机 poll（高维）[gratton2015-2019] / 曲率感知信赖域 DFO（旋转残差）[kim2021]。定位 **高维含噪低预算**。（ADR-0010 澄清：Eldred manifold-sampling 处理**目标非光滑性流形**、非匹配流形，仅借形态。）
  - `ManifoldES`（家族②，主攻押注）：切空间 CMA-ES（ManES）——协方差自动学各向异性、只搜切向不搜法向。备选：ManES 基线 [he2020] / sep-CMA-ES·LM-CMA（高维）[ros2008,loshchilov2014] / active-CMA·VD-CMA（旋转残差）[arnold2010,akimoto2014] / NES（ridge）[nomura2021]。定位 **病态各向异性·多模连续景观**。
  - `ManifoldGA`（家族③，⚠ 蓝本待补充调研）：流形约束的经典遗传算法——连续基因经 `project` 约束在匹配面、离散/组合基因走交叉重组。定位 **组合/离散/混合整数 + 重组式多模全局**；语料 ES 中心、经典 GA 蓝本缺，待用户启动补充调研。
  - `ManifoldBO`（家族④，可选·最低优先级）：几何感知局部 BO——点云＝eoopt anchor 云（`L≪N` 与两级 seam 同构）。备选：graph-GP 点云 [kim2024] / 信赖域局部 TuRBO [eriksson2019] / 低有效维嵌入 [wang2016]。定位 **评价极贵·低有效维/局部子问题**。
  - **跨族共享组件：点云 local-PCA 预条件子**——用廉价 `project` 离线撒 anchor 云、信赖域内 local PCA 估局部各向异性 → 预条件 ManifoldDFO 的 poll / 热启动 ManifoldES 协方差，DFO/ES 共用（把"学各向异性"从在线评价搬到离线 retraction）。
- `ExternalOptimizer`（阶段 5）：把"切向步 + project 重牵引"外壳保留，内部搜索委托给外部求解器（scipy/NLopt/pygmo），让用户能插任意求解器。复用 [baseline/fullspace.py](src/eoopt/baseline/fullspace.py) 的 scipy 集成经验。

### 1.6 多分支层：基础判定（阶段 2）+ 精化分支识别（阶段 7）

- **【阶段 2·基础版】多分支基础判定**（`experiments/branch_probe.py`，扩展 [manifold_starts.py](src/eoopt/experiments/manifold_starts.py)）：全空间采样（**采样范围 + 密度由用户指定**）→ 限步吸引器（`manifold.project` 限步、不要求收敛，[core/types.py:25](src/eoopt/core/types.py#L25) 的 `converged=False` flag）→ 吸引终点**聚类** → 取 **top-k 聚类中心作候选优化起点**（**k 由用户指定**）→ **用户挑具体起点**进入阶段 3 切向优化。**不含**连通性验证/精判——只交付"有几簇、各簇代表点"。
- **【阶段 7·精化版】精化分支识别**：连通性验证、三层判定（投影·局部几何·全局拓扑）、"近邻但不连通"分层判据、KKT 最近点、双投影中点测试、物理离散标签、Pareto 分支筛选等**整体后移、独立为阶段 7**（详见 §三阶段 7，设计基线 ADR-0011 §1–§7）。

`branch_id` 在阶段 2 仅承载"聚类簇编号"占位；升级为真实多分支邻接图 / 奇异连接节点属阶段 7 精化版。

---

## 二、与 lit-review 调研的对齐

最终目标设计的每块都对应 transfer 文档（[transfer-to-electron-optics.md](../references/lit-review-manifold-optimization/transfer-to-electron-optics.md)）的移植卡片：

| 设计块 | transfer 卡片 | 外部成果 | 就绪度 |
|---|---|---|---|
| corrector（已有 `manifold.project`） | A | Berenson 伪逆投影 / Manopt retraction | ★ 已实现 |
| 切空间（已有 `manifold.tangent`） | B | IMACS 零空间 / Romanov SVD | ★ 已实现 |
| MatchingSpec 编译器 | B + 加速器匹配 | 约化 SQP（Nocedal）/ MAD-X MATCH 思想 | ◐ 新建 |
| 双后端 PhysicsBackend | H（Jacobian 使能） | JuTrack AD 思想；EO 侧离散伴随先例 [neustock2019]，但自研矩阵连乘 | ◐ 新建 |
| atlas 多分支精覆盖（已有 `AtlasTracker`） | C | Multifario / atlas-RRT / Porta；加速器切向同伦+折叠换图 [amstutz2017] | ★ 已实现，待多分支实测 |
| 不等式裁剪孤岛 | C+D（边界停止/分叉） | Li–Dankowicz 等式+不等式延拓 | ◐ 新建 |
| 流形内四族优化器（DFO/ES/GA/BO） | E | retraction-based DS [kungurtsev2024] / 切空间 CMA-ES [he2020] / graph-GP BO [kim2024]（调研已定，每族多备选）；经典 GA 待补充调研 | ◐ 新建（GA 待补研） |
| 多分支基础判定（采样-吸引-聚类-topk） | C+D | Xu 解集+图 / equation-free 短突发；加速器多分支先例 [amstutz2017]（组合选取型≠拓扑连通分量） | ◐ 新建 |
| 连通性 CI-NEB（阶段 7 精化的拓扑层） | F | Henkelman CI-NEB / Xu ramping；折叠处换图=chart 邻接先例 [amstutz2017] | ◐ 阶段 7（后移） |
| 鲁棒 CVaR 目标 | E（含噪目标） | equation-free/CBC 噪声关在评估侧 | ◐ 新建 |
| 样本学习流形 | H+数据流形 | AE/diffusion 隐式约束 | ◐ 后期 |
| 可插拔外部求解器 | E | Manopt/RTR + scipy/NLopt | ◐ 新建 |
| Pareto 延拓 | G | Hillermeier / Pareto Tracer | ◐ 路线图后期 |

**三处必须自造的物理特异件**（transfer §四，本项目真正贡献）：
1. 有符号像差平衡目标（`AberrationObjective`，C_s/C_c 符号平衡）。
2. 两级确定性/含噪 seam 作为命名架构（已有，ADR-0001）。
3. EO/加速器专用廉价确定性校正器（双后端的解析一阶模型）。

---

## 三、开发路线图（分阶段，按难度×重要性排序）

> 排序原则：**地基先于扩展、低难度高价值先于高难度、有依赖的按依赖排**。每阶段标注难度（低/中/高）与重要性（高/中）。

### 阶段 1：双表述体系内核重塑（工作流 A，主线）— 难度中，重要性高 · ✅ 已完成（2026-07-28）

**A1** PhysicsBackend 双后端抽象 → **A2** MatchingSpec 编译器 + 内置/自定义 spec → **A3** 领域目标 adapter。
- 内部次序：A1 → A2 → A3（A2 依赖 A1 的后端接口）。
- 产出：EO 与加速器两套表述对等原生支持；C1-C3 平衡、twiss 阈值/指定点、色品匹配可用；用户自定义匹配函数可用。
- ADR-0009：PhysicsBackend 双后端 + MatchingSpec 编译器（同时收纳离焦平衡/C1-C3 选型）。
- **保留自动微分（AD）升级接口**：PhysicsBackend 的 Jacobian 供给当前走复步差分（`ConstraintBase.jacobian`，[constraints/base.py:76](src/eoopt/constraints/base.py#L76)）。A1 显式定义 `jacobian(q)` 供给 seam（后端 Protocol 上），后端可按能力选①复步差分（默认，零工程量）②解析 ③**AD 框架（JAX/autograd，未来升级）**——现在就为 ③ 留位（后端可选实现 `jacobian_ad(q)`，未实现回落复步），日后接 JuTrack 式可微追踪（transfer 卡片 H，[wan2025]）只动后端、不动内核与 MatchingSpec。**EO 侧解析/AD Jacobian 已有同域现成先例 [neustock2019]**（离散伴随，详见 §附"调研现状"与 §六开放问题）。`Objective.value_and_grad` 同留 AD 位（`SpotObjective` 已用复步，[objective/spot.py:52](src/eoopt/objective/spot.py#L52)）。
- 验证：现有 59 测试零回归 + 各 spec 单元测试（算例届时定）+ 各后端 Jacobian 三供给方式一致性（复步 vs 解析 vs AD 若已接）。
- **为何排第一**：是"日后服务两域"的地基，后续所有阶段（多分支在加速器上、DFO、Pareto）都依赖它。AD 接口现在留位，避免日后 JuTrack/可微物理接入时返工内核。
- **完成状态（2026-07-28）**：PhysicsBackend + `ElectronOpticsBackend`/`AcceleratorBackend` 双后端 + `constraints/specs/` MatchingSpec 编译器 + `objective/eo.py`+`accel.py` 领域目标 + AD 供给 seam 均已实现；ADR-0009 已采纳；**59 测试全绿**（含 10 项 ADR-0009，见 [tests/test_adr0009.py](tests/test_adr0009.py)）。

### 阶段 2：多分支结构基础判定（工作流 C）— 难度中，重要性高 · ✅ 已完成基础版（2026-07-29）

**采样-吸引-聚类-topk 基础管线**（用户驱动）：全空间采样 → 限步吸引器 → 聚类 → 取 top-k 聚类中心作候选优化起点 → 用户挑起点。
- **三处用户指定**：初始采样**范围**、采样**密度**、进入备选的聚类数 **k**——均由用户给定。
- **用户挑起点**：聚类完成后**由用户判断**、从 top-k 簇中心里挑具体起点，进入阶段 3 切向优化。
- 产出：给定一个匹配问题，快速给出"**有几簇、各簇代表点**"，交用户选优化起点（**不做**连通性验证 / 可信分支数判定）。
- ADR-0011（§0 基础版）：多分支**基础**判定——采样-吸引-聚类-topk，用户驱动（精化版方法学见阶段 7）。
- 验证：在已知多簇问题上跑通基础管线（算例届时定，候选见 HANDOVER §7.2）。
- **为何排第二**：用户想法③，为阶段 3 切向优化**供多起点**；难度因**只做基础版**下调为中。需阶段 1 的加速器后端才能在加速器多簇问题上跑。**多起点动机（同域佐证）**：电子光学离散伴随反设计 [neustock2019] 自证设计空间"非凸、多局部极小"（"many device designs appear optimal compared to their nearest neighbor in design space"），故须从多个吸引簇各取起点、而非单点下降。
- **完成状态（2026-07-29）**：`experiments/branch_probe.py`（`branch_probe()` + `BranchProbeResult`/`ClusterSummary`）+ `plot_branches` + `tests/test_s6.py` 10 项均已实现，**69 测试全绿**、**内核零改动**、`release/` 镜像已同步。管线 = LHS 盒采样 → `manifold.project` 限步吸引（忽略 converged、按残差近 M 过滤）→ 缩放坐标单链接聚类 + 自动最大间隙阈值（`min_gap_ratio` 护栏）→ medoid 中心 → 按簇大小透明排序取 top-k；随交付 4 条解读免责声明。**关键实现选型（记入 [ADR-0011](adr/0011-multibranch-detection.md) §0.1）**：新增 `keep_in_box` 盒内过滤——Fold/Bifurcation 匹配流形经奇点 (0,0) 全局连通，限步吸引器会把样本拉到盒外顶点区从而两臂短路成一片；只保留盒内吸引终点即实现分支干净分离（簇=盒内吸引盆，非拓扑连通分量）。验证：`Bifurcation`→3 簇、`Fold`→2、`Sphere`/`Linear`/`CurvedEllipse`→1。α 扫大前置小实验 + 真实域多分支基准另起一期。

- **精化分支识别 → 独立为阶段 7**：连通性验证 / 三层判定（投影·局部几何·全局拓扑）/ KKT 约束最近点 / 双投影中点测试 / 物理离散标签 / 不按样本数排序的 Pareto 分支筛选等精化方法学，**整体后移、独立为阶段 7「精化分支识别与连通性判定」**（设计基线 ADR-0011 §1–§7），本阶段不实装。

### 阶段 3：流形内四族切向优化器（工作流 B）— 难度中高，重要性中高 · 🔨 首轮设计完成（2026-07-30，ADR-0010 + 设计 doc）

在 `InManifoldOptimizer` 下并列**四族**新 adapter（与现有 RiemannianTR/PatternSearch/NM 并列，不替代），覆盖不同问题特性。选型已由 `references/algorithm` 调研（[review.md](../references/algorithm/review.md) / matrix.md / reading-list.md，45 included / 6 全文）落定，**每族含多个待开发备选**（唯家族③ 经典 GA 蓝本待补充调研）。

**贯穿四族的两条设计不变量**：
- **① 表示假设门（可移植性判据）**：eoopt 流形是隐式 `c(q)=0` 嵌入子流形、无闭式测地线/exp/特征对 → 只收 **retraction 型**（切步 + `manifold.project`）或**点云型**方法；闭式 geodesic/exp（[colutto2010]）、Laplace–Beltrami 特征对（[jaquier2021]）、齐性空间"运动律"（[dreisigmeyer2017]）型明确排除。理论桥 **[absil2012]**：切步 + 投影回子流形＝合法 retraction ⟹ `manifold.project` 是合法 retraction，retraction 整族有严格落脚点。
- **② 几何各向异性由确定性侧"算"、随机侧只追残差**：`spectrum.py` 每点已算 `J_c` 的 SVD、一阶段 whiten 把 ~100× 压到 κ≈20（ADR-0004）。四族 adapter 都先接受 whiten 切空间坐标、再各自处理残差（理论支撑 IGO 重参数化不变性 [ollivier2013]；机制 Riemannian 预条件 [shustin2023]）。残差仍快速旋转 → 优先无记忆 model-based DFO [kim2021] 而非携带式协方差。

**跨族共享组件 · 点云 local-PCA 预条件子**（源 review §3.7d）：用廉价 `project` **离线**撒 anchor 云 → 信赖域内 local PCA（[shustin2022] 思路）估局部各向异性 → **预条件 ManifoldDFO 的 poll 方向 + 热启动 ManifoldES 协方差**，把"学各向异性"成本从在线（花昂贵评价）搬到离线（花廉价 retraction）。独立开发，DFO/ES 依赖。

**四族备选**：
- **家族① `ManifoldDFO`（主力工作马；针对 高维·含噪·无梯度·低预算）**——三备选：
  - ①a **确定性 poll 直接搜索** [kungurtsev2024]：retraction-based direct search 基线（正生成集 poll + 投影重牵引，含 linesearch 外推、覆盖光滑/非光滑，作者有 GitHub 代码），与现有 `ProjectedPatternSearch` 同族、改动最小 → 基线/低维首选。
  - ①b **概率下降随机 poll** [gratton2015 + gratton2019]：poll 方向以概率 >½ 含下降方向即收敛、方向数与 n 无关；gratton2019 推到盒/线性约束（衔接阶段 4）→ 高维含噪主力变体。
  - ①c **曲率感知 / 模型型信赖域 DFO** [kim2021 + conn2009/audet2017]：每步从函数值重估局部曲率、无记忆状态、对度量旋转鲁棒 → 病态 / 残差快速旋转备选（§3.8 推荐）。
  - 可移植性 **完全**、蓝本 **充分**。语义边界（非备选、仅澄清 ADR-0010）：manifold-sampling DFO [larson2016/khan2018/eldred2023] 处理**目标非光滑性流形**、非匹配流形，仅借形态。
- **家族② `ManifoldES`（主攻押注；针对 病态各向异性·多模·含噪连续景观）**——基线 + 三变体线：
  - ②a **ManES 基线** [he2020]：切空间 CMA-ES + 投影搬协方差 + 只搜切向不搜法向；满秩协方差 O(d²)。CMA-ES 协方差**自动学 31:1 各向异性**——正中 GP 核 / TuRBO 软肋。
  - ②b **大规模变体** [ros2008 sep-CMA-ES / loshchilov2014 LM-CMA]：内禀 ~30 维满秩 O(d²) 偏贵 → 对角(O(d)) / 有限记忆低秩降到近线性 → 高维可扩展。
  - ②c **各向异性追踪变体** [arnold2010 active-CMA / akimoto2014 VD-CMA]：负权主动卸载过时长轴 → 残差旋转缓解。
  - ②d **NES ridge 感知** [nomura2021]：Natural Evolution Strategy 面向"隐式约束 + ridge 结构"，对口 eoopt 硬法向 / 软切向 → CMA-ES 之外的 ES 备选路线。
  - 可移植性 **良好（调研上调）**、蓝本 **充分**；须避开 exp-map 型 [colutto2010] 与 CSA metastability [arnold2014]，由不变量 ② + 一致标架搬运化解。白空间：把 ManES 式切空间 CMA-ES 落到 eoopt 数值投影隐式流形（非矩阵流形）是方法学空白（review §五 gap #2）。
- **家族③ `ManifoldGA`（⚠ 蓝本待补充调研；针对 组合/离散/混合整数变量 + 重组式多模全局）**——机制异于 ES 的单高斯协方差自适应：连续基因经 `project` 约束在匹配面、离散/组合基因走交叉重组，潜在与阶段 2/7 多分支耦合。
  - **薄线索（补充调研起点、非现成蓝本）**：[fong2019] 群体式流形优化（方法论 umbrella）、[he2020] §1 把流形进化归为 PSO/ES/DE 三型（经典交叉 GA 缺席、且都在矩阵流形）。review §五 gap #2 证实"一般隐式约束流形上先进 EA 稀缺"。
  - **待补充调研选型**：切空间 / 组合层交叉-重组算子、离散-连续混合约束处理、与多分支耦合的建群 / 迁移策略。路线图先立族 + 问题域，方法留待调研回填。
- **家族④ `ManifoldBO`（可选·最低优先级；针对 评价极贵·低有效维 / 局部子问题）**——三备选：
  - ④a **graph-GP 点云 BO** [kim2024]：GGP-UCB，流形只需点云（eoopt anchor 云）、无需闭式几何量；`L≪N` 与两级 seam 精确同构、证 regret→0 → 可移植核心。
  - ④b **信赖域局部 BO** [eriksson2019 TuRBO + 几何感知核]：多信赖域局部 GP 绕开全局 GP 高维劣化（旧纯欧氏 TuRBO 冷启动仅 13–47%、须配几何感知核）→ §3.7e 信赖域内局部 graph-GP 合流路线。
  - ④c **低有效维嵌入 BO** [wang2016 REMBO]：目标有效维低时在随机低维子空间做 BO（前置地基小实验测出低有效维则启用）。
  - 可移植性 **部分**、蓝本 **部分**（SQ2 最未闭合）。排除（仅参考）：Riemannian-Matérn / GaBO [jaquier2021/jaquier2019] 需 Laplace–Beltrami 特征对、维数指数、eoopt 隐式流形不可用。

- **前置地基小实验（gating）**：量 eoopt 束斑目标在流形软方向（内禀 ~30 维）whiten 后的**真实有效维数 / 残差各向异性 / 是否慢变**（31:1 是 d=3 旧实测、高维未测）——决定"确定性预条件 + EA/DFO 追残差"混合体成立与否、及四族 / 各备选权重（review §五 #5），并决定 ④c 是否启用。类比 §五(10) 的 α 扫前置小实验。
- **开发顺序**：共享预条件组件 → DFO（①a→①b→①c）→ ES（②a→②b/②c/②d）→ GA（待补充调研）→ BO（可选，④a→④b/④c）。排序依据＝**retraction 原生 vs 几何重建**（review §3.7a–c）：DFO/ES 在流形上"走"、从不"测绘"几何 → 天然绕开维数诅咒；BO 须用点云"重建"几何（graph Laplacian、点数随内禀维指数增长），故排 BO 后——反向，廉价 `project` 又让 BO 从"不可行"变"可选"（`L≪N`≙两级 seam）。
- ADR-0010：流形内四族切向优化器（DFO / ES / GA / BO，每族多备选）+ 表示假设门 + "几何由确定性侧算"原则 + 跨族点云预条件子 + Eldred manifold-sampling 语义边界澄清。**✅ 已建（提议中，2026-07-30）** → [docs/adr/0010-tangent-optimizers.md](adr/0010-tangent-optimizers.md)。
- **首轮开发（2026-07-30，设计完成待实现）**：先做 **ManifoldDFO + ManifoldES 各两员（低维高效 + 高维可用），共 4 个**——DFO `ModelTrustRegionDFO`(①c 低维) + `ProbabilisticDirectSearch`(①b 高维)；ES `ManifoldCMAES`(②a 满秩低维) + `SepManifoldCMAES`(②b 对角高维)；共享 σ-自适应用 he2020 秩和（避 CSA 流形 metastability）。**详细算法规格 + 代码设计**（含补充调研回填的 CMA-ES/sep-CMA/概率下降/模型型 TR 完整式）见 [docs/design/tangent-optimizers-phase3.md](design/tangent-optimizers-phase3.md)。GA（③）/BO（④）本轮不含。
- 前置：`references/algorithm` 四族调研**已完成**（DFO/ES/BO 选型定；家族③ 经典 GA 蓝本待补充调研）；**首轮 4 方法算法细节补充调研已回填设计 doc**（gratton2015/2019 概率下降、conn2009/kim2021 模型型 TR+CARS、hansen2016 CMA-ES 默认式、ros2008 sep-CMA `(d+2)/3` 加速）。
- 验证：四族各与 PatternSearch/NM 在相应基准（高维含噪 / 病态各向异性 / 组合多模 / 极贵少样本）对照（算例届时定）。
- **为何排第三**：与阶段 1/2 正交可并行，但科学紧迫性低于多分支。四族与流形追踪的融合形态＝**每簇内用四族之一做局部切向优化**，多起点由阶段 2 基础判定负责——与 transfer 卡片 E 一致。

### 阶段 4：不等式裁剪孤岛（工作流 A 扩展）— 难度中，重要性中高

**InequalitySpec(g(q)≤0)**：扩展 [continuation/chart.py:39](src/eoopt/continuation/chart.py#L39) 的盒式 `bounds` 为一般 `g(q)≤0`；atlas 延拓在 `g=0` 边界停止/分叉；孤岛与 §1.6 多分支协同。
- 产出：流形被工程不等式切成孤岛的能力——电子光学实测"被工程不等式切成孤岛"（HANDOVER §1）的核心需求。
- ADR-0012：不等式裁剪 + 边界停止/分叉语义。
- 验证：构造已知被不等式切割的流形，验证 atlas 在边界正确停止/分叉。
- **为何排第四**：依赖阶段 1 的 MatchingSpec 编译器与阶段 2 的 atlas 多分支能力；难度中等，但解锁"孤岛=分支"后多分支层的实用性大增。

### 阶段 5：可插拔外部求解器（工作流 A/B 扩展）— 难度低，重要性中

**`ExternalOptimizer`** adapter：切向步 + project 重牵引外壳保留，内部委托 scipy/NLopt/pygmo。
- 产出：用户能插任意求解器——原方案 tier-3 "通用平台"头条诉求的求解器侧。
- 复用 [baseline/fullspace.py](src/eoopt/baseline/fullspace.py) 的 scipy 集成经验。
- ADR-0013：外部求解器 adapter 接口。
- 验证：同一问题用 scipy/NLopt 跑通，与内置优化器对照。
- **为何排第五**：难度低、重要性中，作为"通用平台"的低成本补全；放在阶段 1–4 把内置能力补齐后做，避免过早抽象。

### 阶段 6：鲁棒 CVaR 目标（工作流 A 扩展）— 难度中，重要性中

**`RobustObjective`**：`E[J]+λ·CVaR_α` 包装，CRN 估计。
- 产出：含噪目标下的鲁棒优化——原方案 tier-3 明列项。
- ADR-0014：鲁棒目标包装 + CVaR 估计口径。
- 验证：在含噪 GPT 目标上验证鲁棒解 vs 名义解的差异。
- **为何排第六**：依赖含噪目标（已有 GPT seam）但独立于多分支/DFO；难度中，面向"真实工况鲁棒性"这个进阶需求，非架构头条。

### 阶段 7：精化分支识别与连通性判定（工作流 C 精化 + C3）— 难度高，重要性中高（后移待调研）

把阶段 2 的**基础**多分支判定（采样-吸引-聚类-topk）升级为**可信的分支结构判定**：判"两个吸引簇是否同一分支"，并定量判定分支间连通性。**因方法论仍待厘清、实现复杂度高，整体后移待调研**（设计基线：[ADR-0011](adr/0011-multibranch-detection.md) §1–§7 + 用户方法学规范 [design/branch-identification-methods.md](design/branch-identification-methods.md)）。连通性判定是本阶段"全局拓扑层"的一环，故与精化方法学合并为同一阶段。

**为何基础聚类不够**：欧氏近邻的两个吸引终点族群可能属于不同分支（Porta 2012 命名的"similar RMS distance yet far on the variety"，[matrix.md:17](../references/lit-review-manifold-optimization/matrix.md#L17)）。纯欧氏边权连图会把"近邻但不连通"两支错误短路——Xu 2025 的 Dijkstra+欧氏边权即此陷阱具象先例（`ocr/xu2025_ft.txt:555-627`），**本项目不复制**。正面对照 [amstutz2017]：加速器匹配用**切向同伦追踪**（`dτ/dt`，Eq.9）+ **折叠处（det ∂B/∂τ=0）换校正四极＝换图**，是 C3 延拓侧应效法的机制（惟其多分支是 14 选 6 的**组合选取型**，≠本项目**连续流形的拓扑连通分量**，故不取代采样-吸引-聚类）。

**精化方法学（三层分解，设计基线 ADR-0011 §1–§7）**——关键纪律：连通判定只用便宜确定性 c 及其 Jacobian，含噪 J 绝不参与"是否同支"（与两级 seam 一致）：
- **① 投影层**：**求解器吸引域 ≠ 最近点 Voronoi 分类**（最关键纠偏）——朴素限步 Newton/伪逆得到的是求解器吸引子分类，分到哪支取决于阻尼/信赖域/初值。对策：显式解**约束最近点 KKT** `min ½‖p−x‖²_W s.t. F(p)=0`（`manifold.project` 加可选 KKT 模式）+ 参数度量 `W_ii=1/range²`（度量是问题定义的一部分）。
- **② 局部几何层**：正则/奇异分层（按缩放雅可比数值秩，复用 `manifold.spectrum` σ_min），**奇异点作分支连接节点**（amstutz 折叠换图即此同域先例）；**物理离散标签 ℓ_i**（μ_unwrap / 成像根编号 / 放大率符号 / 本征模连续编号）——防"低阶观测量重合但 μ 差 2π"的误合并。
- **③ 全局拓扑层（＝连通性判定）**：保守建图（参数距离 + 切空间主元角 ‖ΦᵢᵀΦⱼ‖≥cos α + 局部线性一致性 + 同标签）→ 对可疑边做**双投影中点测试**（近平行片层 θ_max≈0 时主元角失效的关键补充：中点分别以 yᵢ/yⱼ 为初值投影，终点分离则判异支、不建边）→ **短程延拓**连通性认证 → 多尺度连通分量稳定性（可选 H₀ 持久同调 + feature-size 带保证阈值，Edwards 2018 / Di Rocco 2022）。
- **分支筛选不按样本数**：`少样本分支 ⇏ 次要分支`（窄吸引域可能含最优解）——多目标比较（吸引域权重 / 内禀规模 / 鲁棒性 Q_0.1{安全半径} / 性能潜力），保留 **Pareto 优势分支**进沿流形优化。

**连通性路线落地（③ 的实现选型）**：①图/Dijkstra（但用便宜 c 侧路径可达、非欧氏边权）/ ②CI-NEB 鞍点定过渡点（[henkelman2000]）/ ③atlas 合并（chart 邻接）。三选一或组合，待调研与阶段 2 实验数据支撑。
- ADR-0011（§1–§7）：三层精化判定方法学（判"是否同支"，连通性验证＝其拓扑层）。**ADR-0015**：连通性算法的选型与实现（③ 的落地）——与 ADR-0011 界定：前者定**判据**、后者定**算法**。
- 产出：可信分支数 + 分支间连通性定量判定 + 最优过渡点。
- 验证：在已知连通/不连通的多分支问题上验证判定正确性（算例届时定）。
- **为何在此（后移）**：依赖阶段 2 基础判定 + 阶段 4 不等式孤岛；方法论未定、复杂度高，故从阶段 2 剥离、整体后移待调研；选型见 §六开放问题。**文献缺口＝本项目方法学贡献点**：未见 2020 年后把"采样-吸引-聚类 + 流形结构验证连通分量"作为命名管线整体发表者。

### 阶段 8：多目标 / Pareto 延拓（工作流 D）— 难度高，重要性中

transfer 卡片 G。`Objective` 扩向量目标或新增 `MultiObjective` seam；`OptResult` 加 Pareto 前沿；Pareto Tracer 延拓。
- ADR-0016：多目标 seam + Pareto Tracer。
- 验证：在多目标 EO/加速器问题上追踪 Pareto 前沿。
- **为何排第八**：难度高、属较前沿组合（"约束流形上的 Pareto 延拓"），待阶段 1–7 把单目标能力夯实后再做。

### 阶段 9：样本学习流形 + 高阶物理扩展（路线图远期）— 难度高，重要性中

- **`SampleLearnedConstraint`**：AE/diffusion 学隐式约束插同一 seam（原方案 tier-3）。
- **高阶物理扩展**：differential-algebra 高阶映射、厚透镜内部截面、浸没靶、外部 3D 场图（原方案 tier-3 物理项，作为 `PhysicsBackend` 可选方法）。
- ADR-0017：样本学习流形接口 + 高阶物理扩展。
- **为何排最后**：难度高、依赖前面所有能力就绪；属"通用平台"的最前沿扩展，非短期必需。

#### 样本学习流形的候选方法（选型见开放问题 4）

- **ECoMaNN**（[arXiv:2006.07746](https://arxiv.org/abs/2006.07746)）：AE 直接学隐式约束 h_M(q)=0，只用 on-manifold 数据 + Local PCA——与本项目已有 atlas anchor 数据天然契合。
- **DLF+DRGD / Landing with the Score**（[arXiv:2509.23357](https://arxiv.org/abs/2509.23357)）：扩散 score 网络给出**可微隐式 retraction**（梯度≈投影、Hessian≈切空间投影子），可替代 `manifold.project`，收敛有非渐近保证。
- **DiffOPT**（Kong et al. 2025）：未知约束优化＝数据流形上采样 π_β∝p(x)·exp[−βh(x)]。
- **选型路径**：AE 系（ECoMaNN，简单、与现有 anchor 数据适配）→ 进阶 score/diffusion 系（DLF/DRGD，可微 retraction、理论保证强）；具体选型待阶段 9 训练数据积累后定（开放问题 4）。

---

## 四、ADR 计划

- **ADR-0009**：PhysicsBackend 双后端（EO/加速器对等，自研传输矩阵）+ MatchingSpec 编译器层 + C1-C3 平衡选型。（阶段 1）
- **ADR-0010**：流形内**四族**切向优化器 adapter（每族多备选）——DFO [kungurtsev2024 / gratton2015-2019 / kim2021] · ES 切空间 CMA-ES [he2020 + ros2008 / loshchilov2014 / arnold2010 / akimoto2014 / nomura2021] · **GA（经典遗传算法，蓝本待补充调研）** · BO 几何感知局部 [kim2024 / eriksson2019 / wang2016，可选] + 表示假设门（retraction / 点云型，桥 absil2012）+ "几何各向异性由确定性侧算"原则 + 跨族点云 local-PCA 预条件子 + Eldred manifold-sampling 语义边界澄清。（阶段 3）**✅ 已建（提议中，2026-07-30）；首轮 = DFO/ES 各两员，设计 doc `design/tangent-optimizers-phase3.md`。**
- **ADR-0011**：多分支结构判定——**基础版**（采样-吸引-聚类-topk，用户驱动，**阶段 2** 实装）+ **精化版**（三层判定 + 连通性验证，§1–§7，后移待调研，**阶段 7**）。
- **ADR-0012**：不等式裁剪 `g(q)≤0` + 边界停止/分叉语义。（阶段 4）
- **ADR-0013**：可插拔外部求解器 adapter 接口。（阶段 5）
- **ADR-0014**：鲁棒目标 `E[J]+λ·CVaR_α` 包装 + CVaR 估计口径。（阶段 6）
- **ADR-0015**：连通性算法（图/Dijkstra · CI-NEB · atlas 合并）的选型与实现——阶段 7 精化分支识别"全局拓扑层"的落地；与 ADR-0011 界定：**ADR-0011 定判据、ADR-0015 定算法**。（阶段 7）
- **ADR-0016**：多目标 seam + Pareto Tracer。（阶段 8）
- **ADR-0017**：样本学习流形 + 高阶物理扩展。（阶段 9）

---

## 五、验证策略（路线图级，算例届时定）

1. **内核零回归**：每阶段结束跑 `uv run pytest -q`（现有 59 测试全绿）。
2. **双后端对称性**：EO 与加速器后端在各自一阶量上复步 Jacobian 有限差分一致性测试。
3. **匹配编译器**：每个内置 spec 的残差 + Jacobian 一致性；`FunctionalSpec` 用户函数 round-trip。
4. **多分支判定**：在已知多分支问题（合成解析流形 / EO 多分支 / 加速器 twiss 多解）上验证分支数正确性——算例留到测试讨论。
5. **不等式裁剪**：构造已知被不等式切割的流形，验证 atlas 边界停止/分叉。
6. **四族对照**：DFO/ES/GA/BO 各与 PatternSearch/NM 在相应基准（高维含噪 / 病态各向异性 / 组合多模 / 极贵少样本）比评价数-精度。
7. **外部求解器**：scipy/NLopt 在同一问题上与内置优化器对照。
8. **鲁棒目标**：含噪 GPT 目标上鲁棒解 vs 名义解差异。
9. **连通性**：已知连通/不连通多分支问题上判定正确性。
10. **前置小实验**（HANDOVER §7.2）：阶段 2 动手前先在现有 n=5 EO 上扫 α 到 80–100 mrad，看单分支 M 是否已多峰，定多分支基准怎么构造。

---

## 六、开放问题（留给后续调研/实验）

1. **精化分支识别与连通性判定的选型（阶段 7，后移待调研）**：三层判定 / 分层连通判据（切空间主元角、同伦探测、CI-NEB、持续同调）/ 双投影中点 / KKT 最近点，及连通性路线（chart 重叠 vs 短延拓可达 vs CI-NEB 鞍点 vs atlas 合并）的选型与阈值——用户明确暂不预设，随**精化分支识别整体后移**（设计基线 ADR-0011 §1–§7；关键纪律已定：连通判定只用便宜 c 侧、J 不参与）。
2. **C1-C3 平衡的解析代理偏小 ~6× 问题**（HANDOVER §7.3 + ADR-0003）：`AberrationBalanceSpec` 落地时用解析 C3 还是 probe-ray c3——选型记入 ADR-0009。
3. **阶段 3 优化器选型 —— DFO/ES/BO 已闭合、GA 与地基待办**：`references/algorithm` 调研（45 included / 6 全文）已定 DFO / ES / BO（各含多备选，见阶段 3、ADR-0010）。**剩余开放**：① **家族③ 经典遗传算法蓝本待补充调研**——语料"进化"覆盖是 ES 中心（[he2020] 归 PSO/ES/DE、经典交叉 GA 缺席；review §五 gap #2 证实一般隐式约束流形上先进 EA 稀缺），薄线索 [fong2019]/[he2020] 可作起点；② **前置地基小实验**——束斑目标在流形软方向 whiten 后的真实有效维/各向异性（决定四族权重与 BO ④c 是否启用，review §五 #5）。
4. **样本学习流形的训练数据来源**（阶段 9）：历史可行设计从哪来、AE vs diffusion 选型——待阶段 1–8 积累足够可行设计后再定。
5. **AD 框架选型**（阶段 1 接口留位）：JAX vs autograd vs 等到 JuTrack/可微物理成熟——接口层现在留位，选型日后定。**新证据 [neustock2019]**：电子光学离散伴随（O(1) 灵敏度、机器精度）已被完整实现，说明 EO 侧 AD/解析 Jacobian **此刻即可行**、不必等加速器 JuTrack 成熟，可据此提前选型。
6. **外部拓扑文献补获**：Edwards 2018 (arXiv:1802.07716)、Di Rocco 2022 (arXiv:2209.01654)、Zahradník 2022 (CTU)、Jaillet–Porta atlas-RRT 期刊版 (IEEE TRO 29(1), 2013) 本库未纳入——若阶段 7 选持续同调或切空间 cycle 路线，按需补获编目。

### 用户决定（本轮 AskUserQuestion，已固化）

1. 想法①程度：重设物理层为双后端（EO + 加速器对等）。
2. 想法②处理：elderd2024=elderd2023 同内容，直接看 elderd2023 设计。
3. 想法③连通性路线：暂不预设。
4. 测试算例：路线设计阶段不关注，留到测试讨论。
5. AcceleratorBackend 一阶量：自研传输矩阵（全可微、复步 Jacobian、与 EO 对称）。
6. DFO 与现有优化器：并列 adapter（不替代）。
7. 原方案 tier-3 全部最终目标项（不等式裁剪、可插拔求解器、鲁棒 CVaR、样本学习流形、高阶物理扩展）均纳入路线图，按难度×重要性排布见 §三。

---

## 附：关键事实核实（讨论前已对代码 + 调研核实）

### 代码现状

- 5 seam + 通用深模块；内核 `manifold/`(project/tangent/spectrum) 仅依赖 ConstraintModel 最小接口。
- PhysicsModel 当前硬绑 EO：[physics/base.py](src/eoopt/physics/base.py) 只有 `transfer_matrix`+`spherical_aberration`；唯一实现 `BzGaussStack`；`unpack_lenses` 是 q→lens 唯一映射。
- 匹配方法只有 `MatchingConstraint`=[B;A−M] 与 `ImagingConstraint`=[B]；无 twiss/色品/C1-C3。
- 目标只有单标量 `value→float`；`SpotObjective`/`GPTSpotObjective`；无多目标、无 CVaR。
- 切向优化器已有 `RiemannianTR`/`ProjectedPatternSearch`/`ManifoldNelderMead`；无 DFO、无外部求解器 adapter。
- branch_id 全程占位透传（[continuation/atlas.py:54](src/eoopt/continuation/atlas.py#L54)），无分支枚举/比较/全局图。
- **不等式只有盒式 bounds**（[continuation/chart.py:39](src/eoopt/continuation/chart.py#L39) `in_bounds`），无一般 `g(q)≤0`。
- 已有"切空间 d-ball 采样 + project + farthest-point 稀疏化"机器：[experiments/manifold_starts.py](src/eoopt/experiments/manifold_starts.py)——想法③的天然起点。
- 基线快速求解器形态：[baseline/fullspace.py](src/eoopt/baseline/fullspace.py)（scipy Nelder-Mead + penalized_scalar）。
- `manifold.project` 已有 `max_iter` 参数（[manifold/project.py:33](src/eoopt/manifold/project.py#L33)）——想法③的"快速吸引器"限步可直接复用。

### 调研现状

- transfer 文档 8 环节移植卡片 A–H + 优先级矩阵（[transfer-to-electron-optics.md](../references/lit-review-manifold-optimization/transfer-to-electron-optics.md)）。
- elderd2024 = elderd2023 期刊版（用户确认同内容）；Eldred manifold-sampling 是**目标非光滑性流形 DFO**，非匹配流形（[review.md:81](../references/lit-review-manifold-optimization/review.md#L81)、[matrix.md:60](../references/lit-review-manifold-optimization/matrix.md#L60)）。
- 加速器匹配现状：MAD-X/elegant/Bmad 把匹配当约束求解求到一个点即止，不追踪解集流形（[review.md:75](../references/lit-review-manifold-optimization/review.md#L75)）；Romanov 2019 IOTA 用 SVD 零空间手动调谐（[review.md:82](../references/lit-review-manifold-optimization/review.md#L82)）。
- Xu 2025 EIC 是加速器真正近邻之一：明确"disconnected branches of the feasible solution manifold"，同伦式解集+图/Dijkstra 连线（非 atlas），自认缺 Jacobian 可由 AD 补（[review.md:76-79](../references/lit-review-manifold-optimization/review.md#L76-L79)）。**其 Dijkstra 用欧氏边权——正是"近邻但不连通"误判的具象先例**（`ocr/xu2025_ft.txt:555-627`）。
- 连通性两条路：Xu 式"采样+图/Dijkstra"（粗）；CI-NEB 式"找鞍点"（精，transfer 卡片 F）。
- **Amstutz 2017（WoS 补获全文）= 加速器第 2 近邻、延拓机制上最贴近**：隐函数定理定义匹配流形 `B=0`（Sp(2N,ℝ)）+ 切向同伦追踪 `dτ/dt`（Eq.9，自称"numerical homotopy method"）+ 折叠处（det ∂B/∂τ=0）换校正四极（换图）+ 6-of-14 多分支 + sFLASH 真机验证；但只为**维持匹配**、无目标/不在流形上优化、无两级 seam（`ocr/amstutz2017/amstutz2017.md`；[review.md:80](../references/lit-review-manifold-optimization/review.md#L80)）。
- **Neustock 2019（WoS 补获全文）= 电子光学离散伴随反设计**：FEM 静电 + Störmer–Verlet 求离散伴随，13,530 参数、O(1) 灵敏度、比有限差分快约 3×10⁴，优化 RMS 束斑(=C_s)；**全空间局部梯度、无匹配流形/延拓/seam**，但**自证**设计空间"非凸、多局部极小"——EO 侧最接近"可微物理/AD-Jacobian"的现成工作（`ocr/neustock2019/neustock2019.md`；[review.md:66](../references/lit-review-manifold-optimization/review.md#L66)）。
- Li–Dankowicz 等式+不等式延拓（[review.md:110](../references/lit-review-manifold-optimization/review.md#L110)）——不等式裁剪孤岛的外部先例。
- **"近邻但不连通"现象与判定**（DeepSeek + Explore 调研 2026-07-27）：Porta 2012 命名（`ocr/porta2012_p1-2.txt:50-54`）；Henderson Multifario 用切空间主元角 ‖Φ_iᵀΦ_j‖≥cos α 判 chart 兼容 + 只覆盖 path-connected 分量（`ocr/henderson2002_ft.txt:49-58,213-228`）；Zahradník 2022 (CTU) 复核 AtlasRRT 半空间约束漏判连通、需主元角修复；持续同调 β₀ + feature-size 保证（Edwards 2018 arXiv:1802.07716、Di Rocco 2022 arXiv:2209.01654）把纯聚类升级为带拓扑保证的分量数推断。详见 §三阶段 7（精化分支识别与连通性判定）。
- **阶段 3 四族切向优化器蓝本台账**（语料 `references/algorithm/`：[review.md](../references/algorithm/review.md) / matrix.md / reading-list.md，45 included / 6 全文）——
  - **DFO**：[kungurtsev2024] retraction-based direct search（JOTA，作者有代码）+ [gratton2015/2019] 概率(可行)下降随机 poll + [kim2021] 曲率感知 DFO。
  - **ES**：[he2020] ManES 切空间 CMA-ES（蓝本）+ 大规模 [ros2008 sep-CMA / loshchilov2014 LM-CMA] + 旋转残差 [arnold2010 active / akimoto2014 VD-CMA] + [nomura2021] NES-ridge。
  - **BO（可选）**：[kim2024] graph-GP 点云（可移植核心）+ [eriksson2019 TuRBO / wang2016 REMBO] 高维逃逸；排除 [jaquier2021] Matérn 特征对。
  - **GA**：⚠ 语料缺经典交叉 GA 流形蓝本（[he2020] 归 PSO/ES/DE、[fong2019] 群体式 umbrella 为薄线索）→ 待补充调研。
  - **理论桥 / 原则**：[absil2012] project＝合法 retraction（表示假设门）；几何各向异性由确定性侧算（[ollivier2013] IGO 不变性 + [shustin2023] 预条件，review §3.8）；retraction 原生 vs 几何重建定四族排序（review §3.7a–c）；跨族点云 local-PCA 预条件子（review §3.7d）。
- **样本学习流形**：ECoMaNN（AE，arXiv:2006.07746）、Landing with the Score / DLF+DRGD（diffusion score，arXiv:2509.23357）、DiffOPT（arXiv 2025）—— `SampleLearnedConstraint` 的方法学来源。
