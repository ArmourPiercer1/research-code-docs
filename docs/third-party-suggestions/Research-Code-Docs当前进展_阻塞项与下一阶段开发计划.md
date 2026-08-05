# Research-Code-Docs 当前进展、阻塞项与下一阶段开发计划

> 仓库：`ArmourPiercer1/research-code-docs`  
> 日期：2026-08-05  
> 决策状态：**停止继续扩张 DQE 测试系统，冻结 DQE v0.4.1 为 advisory evaluator，解耦 Batch 2 与通用 terminal gate，正式进入 Batch 2。**

---

## 0. 执行摘要

当前项目已经出现明显的范围漂移：

- 原始目标是建设一套研究软件文档 Skills 系统；
- 后续为了验证 `documentation-quality-evaluator`，逐步构建了大型 corpus、mutation、双 reviewer、profile pair、三臂对照和 Phase E；
- 这些工作提升了 DQE，但也把“开发一个可辅助后续 Skills 的评估器”扩展成了“在任何后续开发前，先证明一个通用文档准入系统”。

现在需要收缩目标。

最终决策：

```text
DQE_CURRENT_ROLE=ADVISORY_EVALUATOR
DQE_VERSION=0.4.1
DQE_STATUS=EXPERIMENTAL
DQE_TERMINAL_GATE_AUTHORITY=PROFILE_SCOPED
PHASE_E=DEFERRED
BATCH_2=UNBLOCKED
AUTO_TRIGGER=DISABLED
```

核心判断：

> DQE 已经足够作为人工监督下的 advisory evaluator，支持后续 Skills 开发；  
> 它尚不足以作为适用于所有文档类型和所有 profile 的通用自动 terminal gate。  
> 后者不应继续阻塞 Batch 2。

---

# 1. 原始路线中我们在做什么

整个项目的原始路线分为：

- Batch 0：治理与评测基础；
- Batch 1：质量与事实基础；
- Batch 2：文档结构与研究证据适配器；
- Batch 3：三个控制流；
- Batch 4：数值研究软件设计 Skills；
- Batch 5：工作区、文档重构与维护 Skills。

原始路线中并没有 Phase E。

`Phase A–E` 是后来为 DQE 建立内部测试体系时引入的阶段命名。其中 Phase E 指：

```text
current DQE
vs frozen previous DQE
vs no-skill baseline
```

的三臂 admission matrix。

因此：

> Phase E 不是整个 Skills 系统的产品阶段，也不应无限期成为后续 Skill 开发的前置条件。

---

# 2. 当前实际进展

## 2.1 治理与评测基础

目前已经建立：

- Skills registry；
- 系统架构；
- conflict matrix；
- quality-control plan；
- 状态与证据等级词表；
- deterministic checkers；
- 测试 corpus；
- mutation 与 semantic validation；
- blind reviewer A/B；
- aggregation 与 promotion metrics；
- evaluator snapshots；
- bounded execution plan；
- 防止无界 fan-out 的计划校验器。

这部分已经达到并明显超过原始 Batch 0 对“基础评测设施”的要求。

## 2.2 Batch 1 Skills

当前已经存在：

1. `documentation-quality-evaluator`
2. `project-state-reconstructor`
3. `goal-scope-and-workflow-elicitor`
4. `uncertainty-and-decision-manager`

当前共同状态：

```yaml
status: experimental
auto_trigger: false
disable_model_invocation: true
invocation: manual-only-or-orchestrator-only
```

四个 Skill 的 trigger/conflict 基础测试已经通过。

仍未充分完成：

- 后三个 Skill 的 task-quality eval；
- 后三个 Skill 的 reader-test；
- 多个真实项目 shadow run。

## 2.3 Batch 2–5

Batch 2 之后的大部分 Skill 仍只是 registry 中的 `planned` 项。

因此当前项目真实状态是：

> 治理框架和 DQE 评测设施已经相对成熟；  
> 实际功能 Skills 开发仍主要停留在 Batch 1。

---

# 3. DQE 当前能力

## 3.1 已经具备的能力

DQE 已经能够较稳定地：

- 区分 `external`、`legacy`、`controlled`；
- 区分 `audit` 与 `release-gate`；
- 区分 `QUALITY_BAND` 与 `GATE_DECISION`；
- 区分文档生命周期和 claim status；
- 识别混合文档职责；
- 识别状态矛盾；
- 识别 volatile-state contamination；
- 识别不可执行 roadmap；
- 识别裸 claim；
- 识别 evidence-status 问题；
- 输出 finding codes；
- 运行 no-context reader test；
- 输出结构化 verdict；
- 避免 external 文档因为缺本地 frontmatter 而被误杀。

这些都是有效进展。

## 3.2 尚未稳定支持的能力

当前 canary 暴露的未解决 profile 是：

```yaml
artifact_type: experiment-report
provenance_policy: controlled
decision_mode: release-gate
```

对于缺少复现材料的实验报告，DQE 可能同时输出：

```text
QUALITY_BAND=FAIL
READER_TEST=FAIL
GATE_DECISION=ALLOW
```

说明：

> DQE 还没有稳定定义 controlled release-gate 下实验报告的复现完整性准入语义。

这不意味着 DQE 整体不可用。

更准确的结论是：

```text
DQE 对通用文档审查可用
DQE 对部分 profile 的终端准入仍未验证
```

---

# 4. 为什么测试系统消耗不断扩大

最初 DQE 只需要证明：

- 能区分已知好文档和坏文档；
- reader test 可以运行；
- 比 no-skill baseline 更可靠；
- 可以辅助评价后续 Skills。

后续逐步增加了：

- 大型 GitHub seed corpus；
- golden-positive / golden-negative；
- boundary pairs；
- mutation 语义验证；
- 双 reviewer；
- profile pairs；
- 三次稳定性；
- frozen snapshot；
- no-skill baseline；
- finding recall；
- terminal contract；
- checker execution compliance；
- 61-slot 三臂矩阵。

这些设计分别有合理性，但组合后目标发生了变化：

```text
原目标：
得到可用于后续开发的评估器

实际目标：
在开始任何后续 Skill 前，证明一个通用文档验证平台
```

这是范围漂移。

63M-token 事件是运行器事故；更根本的问题是：

> 在尚未积累真实下游 Skill 输出之前，对 evaluator 进行了过早、过广的规格化。

---

# 5. 当前阻塞项

必须区分不同目标。

## 5.1 开始 Batch 2

```text
BLOCKER=NONE
```

只要 Batch 2 Skills 继续保持：

```text
experimental
manual-only
auto_trigger=false
```

就可以开始开发。

当前 DQE 已经足够作为 advisory evaluator，并且可以和人工 reviewer 一起使用。

## 5.2 将 DQE 升级为通用 terminal gate

当前仍有阻塞：

- controlled release-gate experiment report 的复现完整性契约；
- D-17；
- 通用 Phase E admission matrix；
- no-skill 与 frozen-version 对照；
- 对真实下游文档的泛化证据。

这些工作可以延后。

## 5.3 启用自动触发或自动发布

仍然阻塞：

- 每个 Skill 自己的 trigger/conflict/task-quality eval；
- 对目标 artifact profile 的有效验证；
- 真实 shadow run；
- 人工准入；
- DQE 在对应 profile 上具有足够证据。

因此短期内继续保持：

```text
auto_trigger=false
disable_model_invocation=true
```

---

# 6. 当前应作出的开发决策

## 6.1 暂停 DQE v0.4.2 与 Phase E 扩展

暂时不继续：

- `ADR-DQE-002`；
- 结构化 reproducibility contract；
- `reproducibility_contract_check.py`；
- experiment-report complete/incomplete/invalid triad；
- 12-slot canary；
- 新 61-slot Phase E matrix。

这些内容不是错误，但它们实际上属于：

```text
experiment-provenance-and-reproducibility
```

以及正式实验发布体系的领域能力。

该能力原本位于后续 Batch，而不应为了让通用 DQE 完美而提前全部塞进 evaluator。

## 6.2 冻结 DQE v0.4.1

当前建议状态：

```yaml
name: documentation-quality-evaluator
version: 0.4.1
status: experimental
role: advisory-evaluator
terminal_gate_authority: profile-scoped
auto_trigger: false
disable_model_invocation: true
```

## 6.3 明确支持范围

当前支持：

```text
roadmap
ADR
architecture document
technical proposal
evidence note / evidence matrix
external / legacy audit
一般结构、状态、证据与可执行性审查
```

当前未验证：

```text
controlled + release-gate experiment report
通用实验复现发布准入
通用自动 terminal gate
```

对于未验证 profile：

```text
GATE_DECISION=INCOMPLETE
reason=unsupported-evaluation-profile
```

这里的 `INCOMPLETE` 表示：

> 当前 evaluator 没有足够能力给出终端准入结论。

它不是对目标文档质量的直接判断。

## 6.4 延后 Phase E

Phase E 不取消，但改成未来 promotion gate。

重新启动条件：

```text
至少完成两个 Batch 2 Skills
积累 5–10 份真实 Skill 输出
真实输出暴露新的 DQE 失败模式
准备将 DQE 从 advisory 升级为正式 terminal gate
```

届时 corpus 应以真实下游输出为主，而不是继续主要依赖 synthetic mutation。

---

# 7. 下一步开发顺序

## Step 1：治理收尾

只做一个小提交：

1. 更新 roadmap；
2. 更新 registry；
3. 将 DQE 标记为 advisory / profile-scoped；
4. 记录 unsupported profile；
5. 将 Phase E 标记为 deferred promotion test；
6. 保留 v0.4.1 canary 失败证据；
7. 不继续新增 DQE fixtures；
8. 不修改 DQE 判别逻辑。

完成后，DQE 本轮开发冻结。

## Step 2：进入 Batch 2

推荐顺序：

### 2.1 `workspace-forensics-and-inventory`

优先原因：

- `project-state-reconstructor` 已经依赖它；
- 只读，风险低；
- 可以立即应用于真实科研工作区；
- 能持续提供真实测试语料；
- 后续 workspace reconstruction 需要它。

首版能力：

- 文件与目录盘点；
- 入口、测试、实验、结果和缓存识别；
- 孤立脚本与未引用产物识别；
- 潜在 canonical source 识别；
- 不移动、不删除、不修改。

### 2.2 `document-information-architect`

目标：

- 识别混合文档职责；
- 设计 artifact map；
- 分离稳定设计、动态状态、证据和 session record；
- 指定 canonical source；
- 给出拆分、链接和生命周期方案。

它可以直接解决最初混合路线图的问题，也能为 DQE 提供真实、类型清晰的输出。

### 2.3 `research-question-and-literature-planner`

保持为薄适配器：

- 将开放问题转成检索问题；
- 给出检索范围；
- 定义 inclusion/exclusion；
- 定义停止条件；
- 定义证据标准；
- 路由到已有研究 Skills。

不得自行承担广泛检索和综合结论。

### 2.4 `research-evidence-synthesizer`

只消费已取得证据，输出：

- claim–evidence matrix；
- evidence levels；
- transfer assumptions；
- unresolved gaps；
- direct / indirect / analogy / inference 标记。

不得自动启动重型检索。

---

# 8. Batch 2 的测试规模

不要复制 DQE 的大型测试体系。

每个新 Skill 第一轮只要求：

```text
3 个应触发案例
3 个不应触发案例
2 个边界或冲突案例
1 个真实项目 shadow run
1 次 no-context reader test
```

评价方式：

```text
DQE advisory report
+
人工或独立 reviewer
+
一次 no-skill 对比
```

暂时不要求：

- 三版本全 corpus；
- 所有案例三次重复；
- 60+ agent matrix；
- 通用 promotion bar；
- 每个新 Skill 都建立大型 mutation corpus。

只有真实失败出现后，才加入对应 regression case。

---

# 9. 当前状态表

| 项目 | 当前状态 | 是否阻塞 Batch 2 |
|---|---|---:|
| 治理与目录基础 | 基本完成 | 否 |
| Eval harness | 已足够使用，且已有过度扩张倾向 | 否 |
| Batch 1 四个 Skill | 已创建，manual-only | 否 |
| DQE 基础 advisory 能力 | 已具备 | 否 |
| DQE 通用 terminal gate | 未完成 | 否 |
| DQE 实验报告发布准入 | 未定义完整 | 否 |
| Batch 2 四个 Skill | 尚未开发 | 当前真正下一步 |
| 自动触发 | 未准备好 | 只阻塞自动化 |
| Phase E | 延后到 promotion 前 | 否 |

---

# 10. 最短路线

```text
现在
│
├─ 治理提交
│  ├─ 冻结 DQE v0.4.1
│  ├─ 声明支持范围
│  ├─ 标记 unsupported profile
│  └─ Phase E deferred
│
├─ workspace-forensics-and-inventory
│  └─ 真实 workspace shadow run
│
├─ document-information-architect
│  └─ 真实混合文档 shadow run
│
├─ research-question-and-literature-planner
│
├─ research-evidence-synthesizer
│
└─ 积累真实输出后
   └─ 决定是否恢复 DQE Phase E
```

---

# 11. 给本地 Agent 的执行提示词

```text
当前决定是停止继续扩张 DQE 测试系统，正式进入 Batch 2。

执行以下治理收尾：

1. 冻结 documentation-quality-evaluator v0.4.1。
2. 状态保持 experimental。
3. 角色改为 advisory evaluator / profile-scoped gate。
4. auto_trigger=false，disable_model_invocation=true。
5. 明确当前支持：
   - roadmap
   - ADR
   - architecture document
   - technical proposal
   - evidence note/matrix
   - external/legacy audit
6. 明确 unsupported：
   - controlled + release-gate experiment report
   - 通用实验复现发布准入
   - 通用自动 terminal gate
7. 对 unsupported profile：
   GATE_DECISION=INCOMPLETE
   reason=unsupported-evaluation-profile
8. 将 Phase E 标记为 deferred promotion test。
9. 保留所有 v0.4.1 canary 失败证据和 snapshot。
10. 不实施 ADR-DQE-002，不新增 HF-REPRO，不新增 reproducibility checker，
    不运行 12-slot canary，不运行 61-slot Phase E。
11. 更新 creation-roadmap 和 skills-registry，使 Batch 2 与通用 terminal gate 解耦。

然后进入 Batch 2，按顺序开发：

1. workspace-forensics-and-inventory
2. document-information-architect
3. research-question-and-literature-planner
4. research-evidence-synthesizer

每个 Skill 第一轮只做：
- 3 should-trigger
- 3 should-not-trigger
- 2 boundary/conflict
- 1 real shadow run
- 1 no-context reader test
- 1 no-skill comparison

使用：
DQE advisory report + 独立 reviewer
而不是大型 admission matrix。

Phase E 只在以下条件满足后重新考虑：
- 至少两个 Batch 2 Skills 完成；
- 已积累 5–10 份真实输出；
- 准备把 DQE 提升为正式 terminal gate。
```

---

# 12. 最终判断

当前最重要的结论是：

> DQE 已经足够支持后续开发，但不足以承担所有 profile 的自动终端准入。  
> 前者已经达到，后者无需在 Batch 2 前完成。

当前真正的下一步不是继续修 DQE，而是：

```text
把“Batch 2 开发准入”
与
“DQE 成为通用 terminal gate”
在 roadmap、registry 和执行流程中正式解耦。
```
