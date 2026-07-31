<!--
generated_by_skill: (manual, Phase-1 DQE corpus build — decision brief)
skill_version: n/a (corpus dataset_version 3)
source_documents:
  - docs/testing/corpus-build-report.md
  - evals/skills/adjudication/adjudication-2026-07-31.md
  - evals/skills/adjudication/reviewer-{A,B}-2026-07-31.md
  - evals/skills/harness/hard-fail.md (v0.3 anti-erosion rule; HF-9/12A/15)
status: RESOLVED 2026-07-31 (v3 decisions) — D-1=A(FAIL), D-2=A(refine+re-run), D-3=A(clean); D-4 in progress; D-5=A(defer to v0.4+). NEW 2026-07-31 (v4 round): D-6, D-7 OPEN (see bottom).
last_verified: 2026-07-31
-->

# DQE 测试语料 —— 待决策清单（2026-07-31）

> **🆕 v4 追加（2026-07-31，测试升级轮）：D-6（GN-PROP-001 是否有效负例）与 D-7（BP-002-fail 门槛）待你裁决。
> 详见文末 [§v4](#v4-测试升级轮的两项待决策-2026-07-31)。这两项来自两轴盲评双评审 + v0.3 确认性抽测。**


> **✅ 已裁决（2026-07-31）：D-1=A 全部 FAIL · D-2=A 已细化重跑（矛盾已消，盲审 CONTRADICTION=NO）·
> D-3=A 已清理（78/94 一致）· D-5=A 暂缓至 v0.4+。结果：20/20 全部锁为 gold，0 待裁决。D-4（你亲自抽查
> 的范围）见下方 §3 D-4。** 下文保留原始决策背景以备追溯。

> 语料准备（A–F + reviewer G）已完成、确定性检查全绿、15 个案例已达成 gold 共识。**本文件只汇总需要你
> 拍板的事项**；在你决策前，受影响的 5 个案例保持 `candidate`（不作为 gold 使用），盲测矩阵不启动。
> 这些都**不阻塞**已完成的准备工作——只是"把 candidate 锁成 gold / 进入下一轮"之前的收尾裁决。

## 0. 一页速览

| # | 决策 | 选项 | 我的建议 | 影响 |
|---|---|---|---|---|
| **D-1** | 单缺陷负例的 gold 标签定 **FAIL** 还是 **PARTIAL** | A: 全部 FAIL · B: 全部 PARTIAL · C: 逐案 | **A（保持 FAIL）** | 决定 5 个案例能否锁成 gold |
| **D-2** | `GN-PROP-001` 变体的意外二次缺陷 | A: 细化重跑 · B: 接受为双缺陷 · C: 降级弃用 | **A（细化重跑）** | 该负例是否可用 |
| **D-3** | `BP-001-fail` 里附带的 78-vs-69 矛盾 | A: 清理只留 HF-13 · B: 保留 | **A（清理）** | 边界对 BP-001 的"单一差异"纯度 |
| **D-4** | 你亲自抽查哪些案例（治理 §9.4 要求每类型 ≥1） | 见 §附 清单 | 抽查 4–6 份即可 | 语料可信度背书 |
| **D-5**（可选/战略） | 是否给 DQE 增加 **PARTIAL/有条件通过** 档 | A: 保持二元 · B: 加三档 | **暂 A，记为 v0.4+ 议题** | 影响 skill 设计，非本轮 |

---

## 1. 背景（3 句话）

- 语料的用途是**测评 `documentation-quality-evaluator`（DQE）这个 skill**：给它一批已知答案的文档，看它
  判得对不对。
- 我用两个**互相隔离、不加载 DQE skill** 的 reviewer 子代理给 20 个盲测文档独立打标签，A/B **逐案 20/20
  完全一致**（连主缺陷标签都一致）。
- 其中 **15 个** reviewer 判的和语料预期完全吻合 → 已锁 gold；**5 个**出现了一个需要你拍板的系统性分歧
  （下面 §2 是它的根因）。

## 2. 核心张力：同一个"单缺陷负例"，该判 FAIL 还是 PARTIAL？

这 5 个案例都是"**一份很好的文档 + 一处注入缺陷**"。分歧不是"这文档有没有问题"（各方都认同有），而是
**这一处缺陷该不该让整份文档判负**。

**用 `GN-ROADMAP-001` 举例（最典型）：**
- 底稿是一份**优秀的研究路线图**：每个已承诺阶段都有"研究问题 + 最小实验 + 量化指标 + GO/MODIFY/STOP"。
- 注入的**唯一缺陷**：把 Phase-1 的可量化验收门换成"与基线对照，效果达标即可，具体算例与阈值**届时定**"。
  （Phase-2 的门保持完好。）
- **两个盲审 reviewer 都判 `PARTIAL`**：整体很好，只有一个阶段的验收含糊。
- **语料按 DQE 契约判 `FAIL`**：DQE 的 v0.3 硬门 **HF-15**（已承诺阶段的验收不可量化）被命中。

两种判法各自都自洽，差别在**"命中一个硬门"到底等于 FAIL 还是 PARTIAL**：

| 立场 | 主张 | 依据 |
|---|---|---|
| **语料=DQE 契约镜像（FAIL）** | 命中硬门 = 不可降级的 BLOCKER = FAIL | DQE 是**终审门（gate）**，其 v0.3 升级的**全部目的**就是修复"把真实 blocker 降级成 MAJOR 再预测 PASS"的门侵蚀（false-pass）。若 gold 把这些判 PARTIAL，等于奖励 v0.3 刚修掉的行为。reviewer 的 PARTIAL 反而是**好事**——说明缺陷够隐蔽，是强区分样本。 |
| **语料=真实质量基准（PARTIAL）** | 一处缺陷、其余优秀 → 客观上就是"部分合格" | 若把它判 FAIL，语料就比人类判断更严，可能选出/训练出一个**动辄判负**的 DQE。 |

**关键取决于：DQE 的定位是什么？**
- 若是**二元发布门**（放行/拦截）：有未处理的 blocker 就不该放行 → **FAIL 正确**。
- 若是**质量评分器**（打分/建议）：一处小瑕 → **PARTIAL 正确**。
- DQE 的 `SKILL.md` 明确自我定位为 "terminal quality gate"，输出二元 `DOCUMENT_QUALITY=PASS|FAIL`。
  → 因此**我建议 gold 保持 FAIL**（与它的既定角色一致）。若你更想要"评分器"语义，见 **D-5**。

---

## 3. 决策项

### D-1 ｜ 单缺陷负例：FAIL 还是 PARTIAL（**主决策**）

**涉及 4 个案例**（第 5 个 `GN-PROP-001` 另有问题，见 D-2）：

| 案例 | 注入的唯一缺陷 | 命中的门 | reviewer 判 | 语料预期 | 备注 |
|---|---|---|---|---|---|
| `GN-EXP-001` | 删掉复现锚点（commit/环境/版本），保留 74% 结论 | **HF-12A**（承重结论无凭据句柄） | PARTIAL | FAIL | 硬门，FAIL 指向明确 |
| `GN-ROADMAP-001` | 已承诺阶段验收→"届时定" | **HF-15** | PARTIAL | FAIL | 硬门，FAIL 指向明确 |
| `BP-004-controlled` | 同一份 ADR，在 **controlled** profile 下缺溯源 frontmatter | **HF-9** | PARTIAL | FAIL | 硬门；且与 `BP-004-external`(PASS) 构成 profile 对照 |
| `GN-ADR-001` | 删掉 ADR 的 Background/理由，只剩裸规格 | 无硬门（软失败：rationale 锚点） | PARTIAL | FAIL | **四者中最"够呛"的**——无硬门，PARTIAL 最有道理 |

**选项：**
- **A（建议）**：4 个全部保持 **FAIL**。理由：前 3 个都命中硬门，正是 DQE 必须拦下的"好文档 + 一个真
  blocker"形态；`GN-ADR-001` 虽软，但保留 FAIL 才能让 ADR 的"理由锚点"这条非补偿维度有牙齿。
- **B**：4 个全部改判 **PARTIAL**，同时把语料语义从"契约门"改为"质量评分"（需配合 D-5）。
- **C（逐案）**：3 个硬门案例 = FAIL；`GN-ADR-001` = PARTIAL（承认它无硬门）。这是"最忠于证据"的折中。

> 我倾向 **A**；若你希望更贴近 reviewer 的直觉，**C** 是干净的次选。选 **B** 意味着一次 skill 语义转向，
> 建议连同 D-5 一起考虑。

**你的选择：** ☐ A　☐ B　☐ C　☐ 其他：____________



---

### D-2 ｜ `GN-PROP-001` 的意外二次缺陷

- **本意**：从 KEP-127 删掉 Test Plan / Graduation Criteria → 测"提案不可执行"（软失败）。
- **实际**：两个 reviewer 都发现——删了章节，却**留下了 KEP 顶部的 signoff 清单仍勾选"Test plan is in
  place / Graduation criteria is in place"**，凭空造出一个"清单说有、正文没有"的**状态矛盾**。
- 这违反语料政策 §6.3（变体不应引入非目标缺陷；否则降级）。现在它已是 `candidate`。

**选项：**
- **A（建议）**：细化变体计划——连同 signoff 清单里对应勾选一并清掉/置空，再重跑 `generate_mutations.py`
  并重审，使其回到"纯粹缺章节"的单缺陷负例。
- **B**：接受它是一个"缺章节 + 清单矛盾"的**双缺陷**负例，据实改写它的 `required_findings`（不再宣称单缺陷）。
- **C**：弃用该负例，从首批 5 个负例中移除（仍保留其余 4 个）。

**你的选择：** ☐ A　☐ B　☐ C　☐ 其他：____________

---

### D-3 ｜ `BP-001-fail` 附带的数字矛盾（次要）

- BP-001 这组边界对本意只测 **HF-13**（路线图内嵌完整架构+实时状态+会话日志 vs 摘要+链接）。
- 抽验时 DQE 额外正确地抓到：我在 fail 侧写的状态表 `47/47 + 31/47`（合计 78 通过）与正文"69 of 94"**自相
  矛盾**（HF-14a）。这不是坏事（DQE 判得对），但让这组对子的"单一差异"不够纯（fail 侧比 pass 侧多了个矛盾）。

**选项：**
- **A（建议）**：把 fail 侧那句"69 of 94"改成 78，消掉附带矛盾，让 BP-001 只隔离 HF-13。
- **B**：保留——它不影响 BP-001 判负（主因仍是 HF-13），只是附带多一个真实缺陷。

**你的选择：** ☐ A　☐ B　☐ 其他：____________

---

### D-4 ｜ 你亲自抽查的范围（治理 §9.4）

规范只要求你**抽查**、而非逐份通读：每种文档类型至少看 1 份，外加所有"是否算正例"存疑的公开文档。
建议这 **4–6 份**（都附了 reviewer 一句话理由，看起来很快）：

- `GP-PROP-002`（Rejected 的 PEP-2026 判 PASS）—— 确认"决策被否 ≠ 文档质量低"你认可。
- `GP-ADR-001`（Backstage 轻量 ADR，无 Decision/Consequences 标准段）—— 确认它作为**外部 ADR 正例**你接受。
- `GP-ROADMAP-001`（研究路线图判 PASS，HF-15 逃逸）—— 确认"带 GO/STOP 的不确定阶段"算合格。
- 任一负例 + 任一边界对（例如 `GN-EXP-001` + `BP-003`）—— 感受一下缺陷强度。

**你的选择：** 我要抽查：____________（或"信任初审，跳过"）

---

### D-5 ｜（可选 / 战略）要不要给 DQE 增加"PARTIAL / 有条件通过"档

reviewer 一致用 PARTIAL 而非 FAIL，其实指向一个更深的产品问题：**DQE 现在只有二元 PASS/FAIL，可能过粗**。
若增设第三档（如 `CONDITIONAL_PASS`：结构达标但有 1 个必修 blocker），会更贴近人类判断，也能自然化解 D-1 的
张力。但这是一次 **skill 设计变更**，牵涉 verdict schema、下游门禁契约、以及一整轮回归评测。

**选项：**
- **A（建议本轮）**：保持二元，把三档方案记为 **v0.4+ 议题**，先按 D-1 定案推进。
- **B**：现在就立项三档 verdict（会把本轮从"语料准备"扩展成"skill 升级"）。

**你的选择：** ☐ A　☐ B　☐ 其他：____________

---

## 4. 你定了之后，我会做什么（无需你操作）

- **D-1**：更新 5 个（或按你选的子集）manifest 的预期，重跑 `apply_adjudication.py` 把它们锁成 gold（或维持
  candidate）。
- **D-2/D-3**：改对应的 mutation plan / fixture，重跑 `generate_mutations.py` + `validate_case_manifests.py`
  + 重新盲审受影响案例。
- **D-4**：把你的抽查结论记进各 manifest 的 `adjudication.notes`。
- 全部落定后，即可开始**下一轮（盲测矩阵：baseline / v0.3 / v0.2 / 重复×3 → metrics + 回归报告 →
  `experimental→provisional-gate` 提升判定）**。

## 附 ｜ 受影响案例与证据位置

- 完整初审对照表 + 队列说明：[adjudication-2026-07-31.md](../../evals/skills/adjudication/adjudication-2026-07-31.md)
- 两位 reviewer 逐案原文：[reviewer-A](../../evals/skills/adjudication/reviewer-A-2026-07-31.md) ·
  [reviewer-B](../../evals/skills/adjudication/reviewer-B-2026-07-31.md)
- 5 个待裁决案例的 manifest：`tests/corpus/cases/**/{GN-ADR-001,GN-PROP-001,GN-EXP-001,GN-ROADMAP-001,BP-004-controlled}/manifest.yaml`
- 语料全景与验证：[corpus-build-report.md](corpus-build-report.md)

---

## v4 ｜ 测试升级轮的两项待决策 (2026-07-31)

来源：两轴盲评双评审（[adjudication-v4.md](adjudication-v4.md)）+ 未改动 v0.3 评测器的确认性抽测
（[corpus-repair-report-v4.md](corpus-repair-report-v4.md)）。**这两项在你裁决前，对应案例标为 `disputed`、
不进任何 live 指标。** 本轮未改任何 skill。

### D-6 — `GN-PROP-001` 还算不算一个有效负例？

- **现象**：修好悬空 TOC 后，**两位隔离盲评 reviewer 都判 PASS/ALLOW**——他们认为这份 KEP 的 Design
  Details（CRI protobuf、ID 映射算法、idmap 实例、PRR 问卷、失败模式、备选方案）已足够实现，删掉
  Test Plan / Graduation / Rollback 只是"流程脚手架缺失"，不阻塞可执行性。v0.3 评测器判 FAIL，但依据是
  HF-9（external profile 缺口，D-01）+ 一个**新的残留矛盾**（Implementation History 写"1.36 GA"，而签核
  清单里 Test-plan/Graduation 两个 (R) 项是未勾选）——**都不是**本意的"缺验证故事"缺陷。
- **本质**：KEP 基文档太完整，**删一处删不垮它**（与已隔离的 GN-EXP-001/D-04 同一失效模式）。
- **选项**：**A**（推荐）隔离 GN-PROP-001，换一个更精简的 proposal 基文档重建（删掉测试计划就真的不可执行）；
  **B** 像 v1 的 D-1 一样人工判 FAIL；**C** 改写它的"本意缺陷"（例如改测别的东西）。
- **影响**：决定 golden-negative 池里是否保留这个案例；不影响已锁的其余 5 个负例。

### D-7 — `BP-002-fail` 的门槛：单条"稳定文档里的易变事实"该不该 BLOCK？

- **现象**：清掉附带矛盾后，两位 reviewer 都识别出 volatile-in-stable 缺陷（BASELINE 架构文档里裸写
  "当前 69 项测试全部通过"）、质量都判 **PARTIAL**，但**门槛判定分歧**：A=BLOCK（基线参考不该带活跃计数）、
  B=ALLOW（架构理解不受影响，一行不阻塞）。v0.3 评测器触发 **HF-14b（BLOCK）**，与 A + 语料本意一致。
- **选项**：**A**（推荐，维持语料本意）单条 volatile-in-stable 即 BLOCK → gold 保持 FAIL；**B** 视为 MINOR →
  软化为 PASS/ALLOW（则该案例从负例降级）。
- **影响**：决定 BP-002 边界对 fail 侧的 gold；也间接定义 HF-14b 的严格度（会写回 ADR/skill 契约）。

> 裁决后我再执行：若 D-6=A 则重建 GN-PROP-001 并重新双评审；D-7 按你选项锁 gold。**在此之前不动 skill、
> 不跑准入矩阵。**

