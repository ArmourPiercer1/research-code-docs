<!--
generated_by_skill: (manual investigation report)
skill_version_under_test: documentation-quality-evaluator 0.3.0
corpus: dataset_version 3
run: tests/corpus/blind-runs/matrix-2026-07-31 (workflow wf_e8cbf369-027)
source_documents:
  - evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/{metrics.json,evaluation-summary.md,regression-report.md}
  - tests/corpus/blind-runs/matrix-2026-07-31/raw-results.json
  - docs/testing/{corpus-policy,adjudication-protocol,benchmark-changelog,corpus-build-report,decisions-pending-2026-07-31}.md
  - evals/skills/adjudication/*
status: FINAL — DQE v0.3 未达 §17；供用户决定 v0.4 修复优先级
last_verified: 2026-07-31
-->

# 调研报告：documentation-quality-evaluator v0.3 盲测矩阵——方法与结果

## 0. 摘要（TL;DR）

我们为 `documentation-quality-evaluator`（下称 **DQE**，当前 v0.3.0）建成了一套 20 案例的黄金语料，并对其
运行了一次 **26 次隔离盲测矩阵**。**结论：评测流程本身运行成功（26/26、0 报错），而它给出的判定是 DQE v0.3
在 §17 准入门的 7 项指标上全部未达标——因此 v0.3 维持 `experimental`，不予提升为 `provisional-gate`。**

这不是"测试失败"，而是"测试成功地发现了问题"。**⚠️ 关键修正（见 §4X 逐案原文核对）**：把每个失败测试对回
fixture 原文后发现，**多数"失败"其实源于语料 mutation 未干净落地（GN-ROADMAP-001 的 GO 门未删、GN-EXP-001 的
超参/命令未删、GN-PROP-001 的悬空 TOC）或 fixture 过度声明（BP-005-pass/BP-002-fail 的 `status:DECIDED`），
而非 skill 漏判**。**唯一清晰、被受控对照（BP-004 对子）证明的 skill 真缺陷是 HF-9 不认 profile**（次要还有
HF-13 在单一架构文档上过度触发）。因此"是测试不好还是 skill 有问题"的答案是**两者都有，但语料缺陷 > skill 缺陷；
必须先修语料再复跑，才能公平判定 skill 的真实召回**。

**需要你决策的一件事**：下一步范围与顺序（§7 给出 A/B/C 三条路径；结合 §4X 的修正，现在更推荐"先清语料 + 只修
HF-9，再复跑"）。

---

## 1. 背景与目标

- **DQE 的定位**：一个"文档质量终审门（terminal quality gate）"，对研究软件文档（状态报告、路线图、ADR、
  算法规格、证据矩阵等）输出**二元** `DOCUMENT_QUALITY=PASS|FAIL` + 硬门 blocker 列表 + 修复清单。它是整个
  Skills 系统里第一个建成、且用来评测后续所有 skill 的"评分器"，所以必须先把它自己测准。
- **为什么要盲测矩阵**：v0.3 是在一次 hybrid-roadmap "假通过"事故后升级来的，只在极小样本上验证过，其 Batch-2
  门禁资格只是"暂定"。评测流程文档（`docs/documentation-quality-evaluator_测试语料自动准备与评测流程.md`）要求：
  在提升 DQE 之前，必须用一套**独立构造、评测器不参与定标、可盲测、可重复**的黄金语料，跑完 §11 指标并达到
  §17 门槛。
- **本轮目标**：完成语料 → 运行盲测矩阵 → 用确定性脚本聚合 → 对照 §17 给出**通过/未通过**判定。**不**在本轮
  修改 skill 或语料（任何修改都应基于本报告的决策）。

---

## 2. 测试方法（完整链路）

整条链路刻意做成"**评测器看不到答案**"：DQE 每次只拿到一份被随机改名、去掉分类目录、不含预期标签的盲测输入；
预期标签存在评测器读不到的地方，只供聚合脚本使用。

### 2.1 语料构造（20 个黄金案例）

| 类别 | 数量 | 来源 | 构造方式 |
|---|---|---|---|
| golden-positive | 5 | 真实上游（Backstage ADR、K8s KEP-127、Python PEP-2026、Yahoo ResNet recipe）+ 1 合成研究路线图 | 规范化快照 |
| golden-negative | 5 | 由某个 positive 施加**单一缺陷** mutation | 确定性脚本生成 + diff + 断言 |
| boundary-pair | 5 组(10) | 合成/复用，一正一负**只差一个受测条件** | 手写 + 单文件双 profile |

- **溯源可核验**：10 个上游仓库锁定 commit SHA（`UPSTREAM-COMMITS.tsv`），每个种子记录仓库/路径/文件 SHA-256/
  许可证（`seed-register.yaml`），字节级不可变快照 + 校验（14/14 通过）。无许可证的 `mozilla-sre-adrs` 隔离，
  只留引用、不复制正文。
- **单缺陷负例**（关键设计）：负例不是"天然混乱文档"，而是从一个已审定的 positive**只改一处**（删 rationale、
  追加 runbook、删复现锚点、删测试计划、把可量化验收改成"届时定"），并由脚本产出 unified diff + "目标段已改/
  禁改段未动"断言——这样某次判负能归因到**具体缺陷**，而非"整体观感乱"。
- **每案例 manifest 同时声明 `required_blockers` 与 `forbidden_blockers`**：前者是"必须命中的门"，后者是"绝不
  能触发的门"——后者是本套件相对旧内联 yaml 的关键增量，用来抓**硬门过度触发**（评测设计文档说的"无关硬门
  滥用率"）。

### 2.2 数据治理与评测器隔离

- 上游与快照**只读**；一切派生在副本上。公开/知名 ≠ 自动 PASS：种子派生的 positive 在双评审前只是 candidate。
- 规范化**仅限机械操作**（换行/编码/RST 保留），禁止改结论/状态/补论据。
- **评测器绝不参与首次定标**；盲测输入用随机 UUID 命名、剥离分类目录、不含 `expected.*`；映射表放 `.secret/`，
  只供比较器读。**诚实的隔离说明**：本环境没有真正的文件系统沙箱，隔离 = 全新子代理（无主会话上下文）+ 提示词
  层禁止读 manifests/.secret + 强制记录已读文件集。
- 15/20 保留了 holdout 标记（对未来 DQE 调参隐藏标签），防过拟合。

### 2.3 双评审裁决（把 candidate 定为 gold，评测器不参与）

- 两个**互相隔离、不加载 DQE skill/hard-fail/rubric** 的 reviewer 子代理，各自独立审 20 个盲测文档。
- 结果：A/B **逐案 20/20 verdict 一致 + 主缺陷标签一致**（评审可靠性很高）。15 个与语料预期吻合直接锁 gold；
  5 个单缺陷负例被盲审判 **PARTIAL**（整体好、一处缺陷）而语料按 DQE 的"命中硬门=不可降级"契约标 **FAIL**。
- 这 5 个的 FAIL/PARTIAL 边界交由用户裁决：**用户已定 D-1=A（全部保持 FAIL）**，reviewer 的 PARTIAL 在每个
  manifest 里留痕。同时按用户 D-2/D-3 细化了 `GN-PROP-001`（清单矛盾已消）与 `BP-001-fail`（数字矛盾已消）。
  最终 **20/20 gold**。
- **方法学要点**：正因为 reviewer 不知道 HF 门目录，他们的 gold 标签独立于"评测器将被考的那些门"——所以一个
  通过的评测器不是在复读定标者。

### 2.4 盲测矩阵与编排

- 重建盲测套件（因 D-2/D-3 改过 2 个 fixture），生成 26 条运行计划：**v0.3 对 20 案例各 1 次（准入主测）+
  `GN-ROADMAP-001`/`BP-001-fail`/`GP-PROP-002` 各再 2 次（稳定性/三次一致）**。
- 编排用 **后台 Workflow**：26 个隔离子代理并行（并发上限约 10–14），每个 = 全新进程、从磁盘加载 DQE skill、
  跑 `run_checks.py`、走完 HF-1…15、返回**结构化 schema verdict**；工作流在外部按盲测映射回填 case_id 用于
  评分（子代理看不到 case_id/manifest/.secret）。运行：26/26 成功、0 报错、~2.6M tokens、~15 分钟。
  （首次因 `args` 被序列化成字符串失败于 0 子代理、0 token，已修。）
- **本轮范围之外**（§17 不要求、留作后续）：baseline-no-skill（模型自身能力对照）、evaluator-previous v0.2
  （回归对照——且工作区非 git 仓库、v0.2 SKILL 快照已被 v0.3 覆盖，不可直接复现）、全量三次重复。

### 2.5 指标与 §17 门槛（聚合脚本 `aggregate_eval_results.py` 确定性计算）

| §17 指标 | 定义 | 门槛 |
|---|---|---|
| golden-negative 假通过 | 负例被判 PASS 的数量 | = 0 |
| golden-positive 假硬失败 | 正例被判 FAIL 的数量 | = 0 |
| required-blocker 召回 | Σ(命中∩required)/Σ(required)（负例池化） | ≥ 0.90 |
| forbidden-blocker 违规率 | 触发了被禁门的运行数 / 总运行数 | ≤ 0.05 |
| 边界对排序正确率 | pass 判 PASS 且 fail 判 FAIL 的对子 / 5 | = 100% |
| 三次一致性 | 重复运行 verdict 全同的案例 / 稳定性案例 | = 100% |
| 分数标准差(σ) | 稳定性案例总分的最大 pstdev | ≤ 5 |

---

## 3. 结果

### 3.1 §17 七项指标（全部未达标）

| 指标 | 实测 | 门槛 | 结论 |
|---|---|---|---|
| golden-negative 假通过 | **2** | 0 | ❌ |
| golden-positive 假硬失败 | **3** | 0 | ❌ |
| required-blocker 召回 | **0.75** (6/8) | ≥0.90 | ❌ |
| forbidden-blocker 违规率 | **0.115** (3/26) | ≤0.05 | ❌ |
| 边界对排序 | **0.60** (3/5) | 100% | ❌ |
| 三次一致性 | **0.33** (1/3) | 100% | ❌ |
| 最大分数 σ | **6.18** | ≤5 | ❌ |

### 3.2 逐案明细（20 个 current 运行）

标 ⚠️ 为与预期不符的结果。

| 案例 | 类别 | 预期 | 实测 | 命中 blocker | required 召回 | 触发禁门 |
|---|---|---|---|---|---|---|
| GP-ADR-001 | pos | PASS | PASS | — | | — |
| GP-PROP-001 | pos | PASS | PASS | — | | — |
| GP-PROP-002 | pos | PASS | PASS | — | | — |
| GP-EXP-001 | pos | PASS | ⚠️**FAIL** | HF-9 | | —(HF-9 非本例禁门) |
| GP-ROADMAP-001 | pos | PASS | PASS | — | | — |
| GN-ADR-001 | neg | FAIL | FAIL | —(软失败) | | — |
| GN-ADR-002 | neg | FAIL | FAIL | HF-13,14b,12A | 1.0 | — |
| GN-EXP-001 | neg | FAIL | ⚠️**PASS** | （无） | **0.0** | — |
| GN-PROP-001 | neg | FAIL | FAIL | HF-14a,6 | | ⚠️HF-14a |
| GN-ROADMAP-001 | neg | FAIL | ⚠️**PASS** | （无） | **0.0** | — |
| BP-001-pass | b-pass | PASS | PASS | — | | — |
| BP-001-fail | b-fail | FAIL | FAIL | HF-13,14a,14b | 1.0 | — |
| BP-002-pass | b-pass | PASS | PASS | — | | — |
| BP-002-fail | b-fail | FAIL | FAIL | HF-13,14a,14b | 1.0 | ⚠️HF-13,14a |
| BP-003-pass | b-pass | PASS | PASS | — | | — |
| BP-003-fail | b-fail | FAIL | FAIL | HF-6,15 | 1.0 | — |
| BP-004-external | b-pass | PASS | ⚠️**FAIL** | HF-9 | | ⚠️HF-9 |
| BP-004-controlled | b-fail | FAIL | FAIL | HF-9,12A | 1.0 | — |
| BP-005-pass | b-pass | PASS | ⚠️**FAIL** | HF-3,14a | | —(非本例禁门) |
| BP-005-fail | b-fail | FAIL | FAIL | HF-10,12E | 1.0 | — |

正确率概览：**正例 5/5 current 判对了 3 个错 2 个**（另加 BP-004/005-pass 两个边界正例判错，共 20 个 current 里
14 判对、6 判错）。**所有 26 次运行 `CHECKER_STATUS=COMPLETE`、`FACTUAL_VALIDITY=UNVERIFIED`**（源不在工作区，
判 UNVERIFIED 正确）、schema 100% 合法。

### 3.3 边界对排序（3/5）

| 对子 | 测什么 | pass 侧 | fail 侧 | 排序 |
|---|---|---|---|---|
| BP-001 | HF-13 逃逸 | PASS ✅ | FAIL ✅ | ✅ |
| BP-002 | HF-14b | PASS ✅ | FAIL ✅ | ✅（fail 侧另触发禁门，见 D4/歧义B） |
| BP-003 | HF-15 研究逃逸 | PASS ✅ | FAIL ✅ | ✅ |
| BP-004 | external vs controlled 的 HF-9 | ⚠️FAIL | FAIL | ❌（external 该 PASS） |
| BP-005 | HF-12E 假设标注 | ⚠️FAIL | FAIL | ❌（pass 该 PASS） |

两组排序错**都是因为 pass 侧被假失败**（BP-004 因 HF-9-profile，BP-005 因 status:DECIDED 歧义），不是 fail 侧
漏判。

### 3.4 稳定性（1/3）

| 案例 | 三次 verdict | 一致 | blocker Jaccard | 分数 σ |
|---|---|---|---|---|
| BP-001-fail | FAIL / FAIL / FAIL | ✅ | 1.0 | 2.62 |
| GN-ROADMAP-001 | PASS / PASS / FAIL | ❌ | 1.0 | 6.18 |
| GP-PROP-002 | PASS / FAIL / PASS | ❌ | 0.0 | 4.84 |

两例不稳定分别由 **HF-15 边界判断**（GN-ROADMAP-001）与 **HF-9-profile 非确定性**（GP-PROP-002）驱动。

---

## 4. 根因分析（缺陷账本）

> 归属分三类：🔴 **skill 真缺陷/能力缺口**、🟠 **skill 过度严格**、🟡 **语料歧义（该清理，非 skill 问题）**。

### 🔴 D1 — HF-9 不认 profile（最高杠杆）
- **证据**：`BP-004-external`→FAIL[HF-9]（+ forbidden 违规 + 打破 BP-004 排序）；`GP-EXP-001`→FAIL[HF-9]；
  `GP-PROP-002` 重跑2→FAIL[HF-9]（该例唯一不稳定源）。
- **机制**：`frontmatter_check.py`（HF-9）对缺失溯源 frontmatter**无条件**报错；`hard-fail.md`/`SKILL.md` 从未
  指示"在 `provenance_policy: external` 下把 HF-9 降为 MINOR"。DQE v0.3 **根本没有 profile 概念**。
- **性质**：**这是"设计要求 vs 实现缺口"，不是回归**。评测设计文档与 BP-004 明确要求 profile 感知的 HF-9，
  但 v0.3 尚未实现——属于 v0.4 的**能力新增**。BP-004 这组正是为测它而设，如实暴露了缺口。
- **杠杆**：一处修复翻正 **2 个正例假失败 + 1 次 forbidden 违规 + 1 组排序 + 1 例稳定性**。

### 🔴 D2 — HF-12A 召回缺口（致一个负例假通过）
- **证据**：`GN-EXP-001`（删了 git commit/环境/版本、保留"74% 准确率"结论）→**PASS**（总分 76.5），未命中 HF-12A。
- **机制**：删掉复现锚点后，"74%"成了无凭据句柄、无 assumption 标签的承重结论，应触发 HF-12A（doc-only）。评测器
  把它当"仍算完整的 recipe"放行了。
- **杠杆**：修复翻正 1 个负例假通过；召回 6/8→7/8（=0.875，仍需配合 D3 才过 0.90）。

### 🔴 D3 — HF-15 召回 + 稳定性缺口（致一个负例假通过 + 一例不稳定）
- **证据**：`GN-ROADMAP-001`（Phase-1 已承诺阶段验收被改成"届时定"，Phase-2 门完好）→**PASS/PASS/FAIL**。
- **机制**：当**兄弟阶段有好的门**时，评测器漏掉了"单个已承诺阶段验收不可量化"这一 HF-15 命中；判断还不稳定。
- **杠杆**：修复翻正 1 个负例假通过 + 召回至 8/8=1.0 + GN-ROADMAP-001 稳定性。

### 🟠 D4 — HF-13 / HF-14a 过度触发（forbidden 违规 11.5% > 5%）
- **证据**：`BP-002-fail` 触发 HF-13+HF-14a（均为该例禁门）；`GN-PROP-001` 触发 HF-14a（禁门）。
- **机制**：`BP-002-fail` 只是一份带"成熟度快照"的架构文档，并非"≥2 个不同生命周期的正文角色"——HF-13 属**过度
  分类**；`GN-PROP-001` 删章节后 **TOC 仍列着被删章节的锚点**（悬空），被误读成状态矛盾（HF-14a）。
- **注意**：`BP-002-fail` 的 HF-14a **部分是语料诱发**（见歧义 B），HF-13 才是纯 skill 过度触发。

### 🟡 语料歧义 A — BP-005-pass
- **证据**：`BP-005-pass`→FAIL[HF-3,HF-14a]（该 PASS）。
- **机制**：fixture 的 frontmatter 写了 `status: DECIDED`，正文却是明确标注的 `HYPOTHESIS（尚未验证）`——一份
  "DECIDED"的证据笔记里装着未验证假设，本身是混合信号，诱发 HF-3（假设当已决）。**这是 fixture 的问题**，不能
  全算 skill 头上。
- **修法（语料）**：把 BP-005-pass 的 status 改为非 DECIDED（或去掉），让唯一受测信号是"诚实的假设标注"，从而
  干净地隔离 HF-12E。

### 🟡 语料歧义 B — BP-002-fail
- **证据**：`BP-002-fail` 触发 HF-14a（我把它列为禁门）。
- **机制**：fixture 写了 `status: DECIDED`+"The core is done"，却又有 `OQ-2` "design review in progress"——这是
  **真实的附带矛盾**，所以 HF-14a 的触发**部分合理**（与之前 GN-PROP-001 清单矛盾同类）。本意的唯一缺陷是 HF-14b。
- **修法（语料）**：去掉"core is done/DECIDED"的过度声明让 HF-14b 成唯一缺陷；或承认 HF-14a 为第二个预期 blocker、
  将其移出 `forbidden_blockers`。

> **横切模式**：歧义 A、B 与之前 GN-PROP-001 都是同一个"**`status: DECIDED` 过度声明**"反模式——合成 fixture 时
> 惯性地写了 DECIDED，与"未验证/未完成"内容冲突。清理时应统一排查所有合成 fixture 的 status 字段。

---

## 4X. 逐个失败测试：应发现/不应发现 + 原文段（test-vs-skill 判断依据）

> **逐案核对 fixture 原文后有一个重要修正**：本轮"6 个判错 current + 2 处 forbidden 触发"里，**多数其实源于
> 语料 mutation 未干净落地或 fixture 过度声明，而非 skill 漏判**。唯一清晰、被良好隔离证据支持的 skill 缺陷是
> **HF-9 不认 profile**。下面逐案给出"应/不应发现的点 + 原文段 + 归属"，供你自己判断。归属图例：🔴 skill 真缺口 ·
> 🟠 skill 偏严/误分类 · 🟡 测试问题（fixture 或 forbid 设置）。

### FT-1 · GP-EXP-001 —— 正例被判 FAIL[HF-9]（误报）
- **不应发现**：这是一份 `external` 的 Yahoo 复现 recipe，缺"本地溯源 frontmatter"在 external profile 下最多
  是 MINOR，不应硬失败。
- **原文段**（fixture 第 1 行，开头无 `<!-- ... -->` 溯源块）：
  > `# Train ResNet-50 on ImageNet`
- **归属**：🔴 **skill 缺口**（DQE v0.3 无 profile 概念，`frontmatter_check.py` 无条件报 HF-9）。属"设计要求、
  v0.3 未实现"的新能力，非回归。测试预期本身是站得住的（设计与 BP-004 都要求 external 宽免）。

### FT-2 · BP-004-external —— 正例被判 FAIL[HF-9]，且触发禁门（误报）
- **不应发现**：与 `BP-004-controlled` **同一字节**，这组对子的唯一受测变量就是 profile：external 侧 HF-9 不应
  触发，controlled 侧应触发。skill 两侧都判 FAIL，只对了 controlled。
- **原文段**（第 1 行，无溯源块；正文是完整规范的 ADR：Context/Decision/Consequences/Alternatives 齐备）：
  > `# ADR 7 — Use content-addressed cache keys for the build graph`
- **归属**：🔴 **skill 缺口——最干净的证据**。同文档双 profile 的受控对照，直接证明 skill 需要 profile 感知。
  **这条几乎可以单独定性 skill 有真问题。**

### FT-3 · BP-005-pass —— 正例被判 FAIL[HF-3,HF-14a]（误报，混合）
- **不应发现**：正文把结论**显式标注为未验证假设**，HF-3（假设写成已决事实）不应在该 claim 上触发。
- **原文段**（claim 标注得很清楚，第 14/16/24 行）：
  > `- **HYPOTHESIS (尚未验证):** the projected-gradient variant is more stable than the baseline...`
  > `  - **Evidence status:** \`project-inference\` — no in-project experiment has been run yet.`
  > `We do **not** assert the variant *is* more stable — only that it is a hypothesis worth the experiment...`
- **但** fixture frontmatter 却写（第 6 行）：`status: DECIDED`
- **归属**：🟡+🟠 **混合**。fixture 的 `status: DECIDED` 与"通篇是未验证假设"的正文冲突，诱发了 HF-3（**测试该清理**
  —— 一份只装假设的证据笔记不该标 DECIDED）；同时 skill 过度看重 frontmatter status、忽略正文强假设标注（**skill
  偏严**）。**倾向：先清 fixture，再看 skill 是否仍误报。**

### FT-4 · GN-EXP-001 —— 负例被判 PASS，漏 HF-12A（漏报，但 mutation 偏弱）
- **应发现**：删掉复现锚点后，"74% 准确率"应成"无凭据句柄、无 assumption 标签"的承重结论 → HF-12A。
- **原文段**：
  > 结论保留（第 85 行）：`The top-1 single crop accuracy is 74.0% after 500K iterations.`
  > Code 段已无 commit（第 36 行）：`The code is written using TensorFlow and uses its high level APIs...`
  > （原句 "We ran our experiments using git commit \`24b236...\`" 已删除）
  > **但**训练命令与全套超参仍在（第 39、57–61 行）：`python train.py --dataset_directory=...` /
  > `SGD momentum 0.9 · batch 256 · LR 0.1 decayed after 150000,300000,...`
- **归属**：🟡→🟠 **主要是测试偏弱**。mutation 只删了 commit/版本/硬件，却**留下完整训练命令 + 超参 + LR 计划**，
  方法仍大体可循 —— "74% 无 commit"是比预期弱得多的 HF-12A，评测器判 PASS（总分 76.5）**有其道理**。要干净测
  HF-12A，应连超参/命令一并移除，或把结论改写成明显无支撑的断言。

### FT-5 · GN-ROADMAP-001 —— 负例被判 PASS/PASS/FAIL，漏 HF-15（漏报，但 mutation 有缺陷）
- **应发现**：已承诺 Phase-1 的验收不可量化 → HF-15。
- **原文段**（Phase-1，第 17/23/24 行）：
  > `## Phase 1 — feasibility probe (research) · committed · next`
  > 注入的含糊行：`- **验收（committed · next）：** 与基线对照，效果达标即可，具体算例与阈值届时定。`
  > **但可量化 GO 门仍在**：`- **GO:** ≥ 20% error reduction on the held-out Re → proceed to Phase 2.`
- **归属**：🟡 **主要是测试缺陷**。mutation 本应"用含糊验收替换可量化门"，实际只删了 MODIFY/STOP 两行——我的
  正则 `^\s*\*\*(GO|MODIFY|STOP):\*\*` 匹配不到带短横线前缀的 `- **GO:**` 行，于是 **GO ≥20% 门被保留**。该阶段
  同时有"含糊行 + 可量化 GO"，并非真正不可量化 → 评测器判 PASS / 不触发 HF-15 **是可辩护的**。**这条几乎不能算
  skill 漏判**（三次里 1 次 FAIL 恰说明它处在边界）。

### FT-6 · BP-002-fail —— 判 FAIL 正确，但触发禁门 HF-13+HF-14a（过度触发，混合）
- **原文段**：
  > 本意缺陷 HF-14b（裸活跃计数、无动态源指针，第 28 行）：`当前 69 项测试全部通过，...三个模块都已就绪。The core is done.`
  > 但同页有真实矛盾：frontmatter `status: DECIDED` + "The core is done" ⟷ `OQ-2: ...(design review in progress)`（第 32 行）
- **归属**：**HF-14a = 🟡 测试问题**——fixture 确实自相矛盾（"已完成" vs "评审进行中"），HF-14a 触发**合理**，是
  我把一个真实缺陷错列进了 `forbidden_blockers`；**HF-13 = 🟠 skill 过度触发**——单一架构文档 + 一个成熟度快照，
  并非"≥2 个不同生命周期的正文角色"，不该判混合。

### FT-7 · GN-PROP-001 —— 判 FAIL 正确，但触发禁门 HF-14a（过度触发，混合）
- **原文段**（删了章节，但 TOC 仍列锚点，第 3/30/36/45 行）：
  > `<!-- toc -->` … `- [Test Plan](#test-plan)` / `- [Graduation Criteria](#graduation-criteria)` /
  > `- [Feature Enablement and Rollback](#feature-enablement-and-rollback)`（而正文中这些章节已删除）
- **归属**：🟡+🟠 **混合**。mutation 删了章节却**未删对应 TOC 条目**，留下悬空锚点（**测试该清理**）；skill 把
  "TOC 有、正文无"误判成 HF-14a"状态矛盾"，但 HF-14a 定义是"互相矛盾的状态数值(测试数/完成度/日期)"，悬空导航
  ≠ 状态矛盾（**skill 误分类**）。

### FT-8 · GP-PROP-002 —— 正例 PASS/FAIL/PASS 不稳定，repeat-2 触发 HF-9（误报，稳定性）
- **原文段**（PEP 头是 PEP 自有元数据，非 skill 溯源 frontmatter）：
  > `PEP: 2026` / `Status: Rejected` / `Type: Process`（全文无 `<!-- skill_version... -->` 块）
- **归属**：🔴 **skill 缺口 + 不稳定**（同 FT-1/FT-2）。external 下缺 skill-frontmatter 不应硬失败；且三次里两次
  放行、一次因 HF-9 失败，说明 external 宽免的应用**本身不稳定**。

### 归属修正表（更新 §4 的初判）

| 失败项 | §4 初判 | 核对原文后归属 |
|---|---|---|
| GP-EXP-001 · HF-9 | 🔴 skill | 🔴 skill（profile 缺口，新能力） |
| BP-004-external · HF-9 | 🔴 skill | 🔴 skill（**最干净证据**） |
| GP-PROP-002 · HF-9(不稳定) | 🔴 skill | 🔴 skill |
| BP-005-pass · HF-3/14a | 🟡 fixture | 🟡+🟠 混合（fixture `status:DECIDED` 为主） |
| GN-EXP-001 · 漏 HF-12A | 🔴 skill | 🟡→🟠 **主要测试偏弱**（超参/命令未删） |
| GN-ROADMAP-001 · 漏 HF-15 | 🔴 skill | 🟡 **主要测试缺陷**（GO 门未删） |
| BP-002-fail · HF-14a(禁门) | 🟠 skill | 🟡 测试（forbid 了真实矛盾） |
| BP-002-fail · HF-13(禁门) | 🟠 skill | 🟠 skill 过度触发 |
| GN-PROP-001 · HF-14a(禁门) | 🟡+🟠 混合 | 🟡+🟠 混合（悬空 TOC + 误分类） |

**修正后的核心结论**：
1. **唯一清晰、隔离良好的 skill 缺陷 = HF-9 不认 profile**（BP-004 对子干净证明 + 2 个 external 文档佐证 + 稳定性
   佐证）。这条**确定是 skill 真问题**。
2. **HF-13 在单一架构文档上过度触发** = 次要但真实的 skill 偏严。
3. **两个"负例假通过"(GN-EXP-001 漏 HF-12A、GN-ROADMAP-001 漏 HF-15) 主要是 mutation 未干净落地**——超参/命令、
   GO 门被保留，导致 fixture 并没有真正呈现目标缺陷。**这两条在清理语料前，不能算作 skill 漏判。**
4. 因此，是"测试不好"还是"skill 有问题"的答案是**两者都有，但比例是：语料缺陷 > skill 缺陷**。**必须先修语料、
   再复跑，才能公平判定 skill 的真实召回**。

---


**为什么这些发现可信（构造效度）**
- 评测器全程盲测、从磁盘加载真 skill、每次真跑 checker（26/26 COMPLETE）、schema 100% 合法——这是被测 skill 的
  **真实行为**，不是提示词伪影。
- 预期标签由**不加载 DQE 的独立双评审**（20/20 一致）+ 用户裁决定出，评测器未参与定标——发现的偏差是评测器
  相对独立基准的偏差。
- 关键缺陷有**成对/重复证据**：HF-9 在 3 个独立 external 文档上一致误触发；两个负例假通过各有明确漏判的门。

**混淆与需扣除的部分（内部效度）**
- 6 个判错的 current 结果里，**并非全是 skill 缺陷**：`BP-005-pass`（歧义 A）与 `BP-002-fail` 的 HF-14a（歧义 B）
  至少部分由 fixture 诱发。**扣除语料歧义后，纯 skill 缺陷是 D1（HF-9，致 GP-EXP-001/BP-004-external/GP-PROP-002）
  + D2（GN-EXP-001）+ D3（GN-ROADMAP-001）+ D4 的 HF-13 过度触发**。即便如此，负例假通过=2、召回 0.75、稳定性 1/3
  等**硬性未达标项与语料歧义无关**，结论稳健。
- HF-9-profile 是"**新需求**"：v0.3 从未承诺过 profile 感知，语料引入了这条设计要求。这不削弱发现（缺口真实），
  但决定了它是"**特性新增**"而非"修 bug"。

**方法本身的局限（外部效度/充分性）**
1. **样本小**：20 案例、每类型 2–5 个，评测设计文档 §11.4 明确说"不应把这些数字当统计充分，只作工程准入门"。
2. **单模型、单轮**：只测了当前会话模型的 DQE 行为；未做 baseline-no-skill（无法量化"skill 相对裸模型的增益"
   这一 Batch-1 里程碑）、未做 v0.2 回归对照（v0.2 快照不可复现）。
3. **稳定性样本极小**：三次一致性/σ 只基于 3 个案例，σ≤5 这类阈值在 n=3 上噪声大；GP-PROP-002 的 σ 主要由 HF-9
   非确定性放大。
4. **隔离非真沙箱**：靠"全新子代理 + 提示词禁令 + 读文件审计"，非文件系统级隔离（已如实声明）。
5. **指标定义的边界**：forbidden-blocker 违规率把"部分由语料诱发的触发"也计入；召回是负例池化、对少数漏判敏感。
6. **profile 只在提示词里告知**：评测器靠提示词里的 `provenance_policy` 字段感知 profile，而非 skill 内建流程——
   即使 v0.4 修好 HF-9，仍需决定 profile 如何进入 skill 的稳定契约（见 §7 注）。

---

## 6. 评测器做对了什么（避免以偏概全）

- **8 个负例判负且命中正确的门**：HF-13（BP-001-fail、GN-ADR-002）、HF-14b（BP-002-fail）、HF-15（BP-003-fail）、
  HF-12E（BP-005-fail）、HF-9-controlled（BP-004-controlled）、软失败（GN-ADR-001、GN-PROP-001）。
- **HF-13/14b/15/12E 的 escape hatch 在干净正例上都放行**：GP-ROADMAP-001（HF-15 研究逃逸）、GP-PROP-001（长
  文档不因长度扣分）、GP-PROP-002（Rejected 不等于低质量）、BP-001/002/003-pass。
- **纪律遵守**：全程未预测 re-eval PASS、未把无源的 HF-12 报成 verified、把嵌入文档的指令当内容而非命令。
- 综合：DQE v0.3 **约 70% 判对**，缺陷是**少数可定位、可修复**的门，而非整体失效。

---

## 7. 建议与修复杠杆

### 7.1 每项修复对指标的预期影响

| 修复 | 类型 | 预期翻正 |
|---|---|---|
| **F1 HF-9 profile-gating**（external⇒HF-9 为 MINOR，controlled⇒blocker） | skill | 正例假失败 3→1、forbidden 3→2、排序 3→4/5、稳定性 1→2/3 |
| **F2 HF-12A 结论-凭据召回**（无复现句柄的量化结论） | skill | 负例假通过 2→1、召回 0.75→0.875 |
| **F3 HF-15 逐阶段召回**（任一已承诺阶段验收不可量化即命中，与兄弟无关） | skill | 负例假通过 1→0、召回→1.0、GN-ROADMAP-001 稳定 |
| **F4 HF-13/14a 收紧**（HF-13 需≥2 正文角色；悬空 TOC≠矛盾） | skill | forbidden 违规→(接近)0 |
| **C1 清理 BP-005-pass** status:DECIDED | 语料 | 正例假失败→0、BP-005 排序→对 |
| **C2 清理 BP-002-fail** 过度声明 | 语料 | 去掉附带 HF-14a、fail 侧只剩 HF-14b |

**F1+F2+F3+F4+C1+C2 全做**：预期 7 项全绿（负例假通过 0、正例假失败 0、召回 1.0、forbidden≈0、排序 5/5、
稳定性 3/3、σ 需复跑确认）。

### 7.2 三条候选路径（供决策；已按 §4X 修正）

> 修正要点：F2/F3 原以为是 skill 召回缺口，逐案核对后**主要是 fixture 没把缺陷做实**（GO 门/超参未删）。所以
> 它们现在首先是**语料重做**任务（把 mutation 补干净），复跑后**仍**漏判才升级为 skill 问题。

- **路径 A′（修正后推荐）——先清语料 + 只修 HF-9，再复跑判定**：
  1. 语料：重做 `GN-ROADMAP-001`（连 `- **GO:**` 行一并替换为含糊验收）、`GN-EXP-001`（把超参/命令一并抹掉或把
     结论改为无支撑断言）；清 `BP-005-pass`/`BP-002-fail` 的 `status:DECIDED`、补删 `GN-PROP-001` 的悬空 TOC；把
     `BP-002-fail` 的 HF-14a 从 `forbidden` 移出（或去掉那处矛盾）。
  2. skill：只改 **F1 HF-9 profile-gating**（最高杠杆、唯一确定的 skill 缺陷）+ 顺带收紧 **F4 的 HF-13**（单一
     架构文档不算混合）。仅升 DQE 到 0.4.0。
  3. 复跑同一 26 次矩阵。**预期**：正例假失败→0、边界排序→5/5、稳定性→2–3/3；负例假通过是否归零，取决于语料重做
     后 DQE 是否真能命中 HF-12A/HF-15——**这才是对 skill 召回的公平考试**。复跑后仍漏判的，才立项 F2/F3 skill 修复。
- **路径 B（你先审再定）**：你基于本报告（尤其 §4X 原文段）逐条判"这算 skill 问题还是测试问题"，指定处置，我再执行。
- **路径 C（最省，仅验证最高杠杆）**：**只修 F1（HF-9）**、其余不动，复跑。预期只翻正 HF-9 相关的 3–4 个结果
  （正例假失败 3→1、排序 3→4/5、稳定性 1→2/3），负例假通过与语料诱发项不变——用于**单独确认 HF-9 修复的真实
  收益**，再决定要不要投语料重做 + F4。

> 说明：**不推荐**原"路径 A 全量按 F1–F4 当 skill 缺陷来修"——那会把本属语料缺陷的 F2/F3 误当 skill 改，可能过度
> 修改 skill。正确顺序是先让 fixture 真正承载缺陷，再考 skill。

> **注（给 v0.4 的设计决定）**：profile 目前只经提示词字段传入。v0.4 若引入 profile 感知，需决定 profile 如何进
> DQE 的稳定契约——是作为 skill 输入参数、还是让 skill 从文档/调用方推断。这会影响下游门禁契约，建议连同 F1 一并
> 设计。另可考虑 D-5（给 verdict 增设 PARTIAL/CONDITIONAL 档）——它能同时缓解"单缺陷负例 FAIL/PARTIAL"张力，但
> 是更大的 schema 变更，本轮已暂缓至 v0.4+。

### 7.3 无论选哪条，建议随手补的方法改进
- 清理**所有**合成 fixture 的 `status` 字段（排查 DECIDED 过度声明反模式）。
- 若要量化"skill 增益"，补一轮 **baseline-no-skill**（§8 里程碑要求 DQE 胜过裸模型）。
- 扩大稳定性样本（≥5 案例×3）再收 σ 阈值，减小 n=3 噪声。

---

## 8. 复现与产物清单

**一键复跑（v0.4 或改语料后）**：
```
# 1) 重建盲测套件（若改过 fixture）
.venv/Scripts/python.exe scripts/build_blind_suite.py --all --run-id <new-id> --seed 2026
# 2) 生成 26 次运行计划
.venv/Scripts/python.exe scripts/make_eval_plan.py tests/corpus/blind-runs/<new-id> \
    --stability GN-ROADMAP-001 BP-001-fail GP-PROP-002 --repeats 3
# 3) 用 <new-id>/eval-plan.json 作 args 跑 Workflow（脚本见 workflows/scripts/dqe-blind-matrix-*.js）
# 4) 写回 raw-results.json 后聚合
.venv/Scripts/python.exe scripts/aggregate_eval_results.py \
    tests/corpus/blind-runs/<new-id>/raw-results.json --out <results-dir>
```

**本轮产物**
| 内容 | 路径 |
|---|---|
| 原始 26 条 verdict | `tests/corpus/blind-runs/matrix-2026-07-31/raw-results.json` |
| 指标 JSON | `evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/metrics.json` |
| 结果汇总 | `.../evaluation-summary.md` |
| 回归报告（简版） | `.../regression-report.md` |
| 运行计划 | `tests/corpus/blind-runs/matrix-2026-07-31/eval-plan.json` |
| 语料/治理/裁决 | `docs/testing/*`、`evals/skills/adjudication/*`、`tests/corpus/**` |
| 脚本 | `scripts/{build_blind_suite,make_eval_plan,aggregate_eval_results,generate_mutations,...}.py` |

---

## 9. 结论

评测基础设施本轮**验证成功**：可端到端产出可核验、可盲测、可重复、确定性聚合的判定。它给出的结论是
**DQE v0.3 未达 §17 准入门，维持 experimental**，并把失败原因收敛到 **3 个真实 skill 缺陷（HF-9 profile、
HF-12A/HF-15 召回）+ 1 类过度触发（HF-13/14a）+ 2 处语料歧义**，其中 HF-9-profile 是最高杠杆。扣除语料歧义后
结论依然稳健。方法本身的主要局限是样本小、单模型、缺 baseline/v0.2 对照——数字应作**工程准入门**而非统计充分性
结论。请基于本报告选择 §7 的修复路径（A/B/C），我据此执行 v0.4 修复与复评。
