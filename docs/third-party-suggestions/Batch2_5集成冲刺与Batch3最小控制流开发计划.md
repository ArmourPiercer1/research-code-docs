# Batch 2.5 集成冲刺与 Batch 3 最小控制流开发计划

> 仓库：`ArmourPiercer1/research-code-docs`  
> 日期：2026-08-05  
> 当前状态：Batch 2 四个 Skill 已完成 MVP 与轻量首轮测试；下一步进入 Batch 2.5 集成冲刺。  
> 决策：**先验证原子 Skill 接口，再进入 Batch 3 最小控制流骨架。**

---

## 0. 执行摘要

Batch 2 的四个 Skill 已经完成：

- `workspace-forensics-and-inventory`
- `document-information-architect`
- `research-question-and-literature-planner`
- `research-evidence-synthesizer`

它们均已通过轻量首轮验证：

```text
trigger: 32/32
shadow runs: 4/4
reader discipline checks: 4/4
no-skill comparisons: 4/4 显示明确边界价值
```

当前最缺的不是继续增加单体测试，而是验证：

> 一个 Skill 的输出，能否在不依赖聊天上下文的情况下，被下一个 Skill 正确消费。

因此下一阶段采用：

```text
Batch 2.5：两条真实集成链 + 最小接口冻结
→ 修订控制流架构表述
→ Batch 3：三个最小控制流骨架
```

不立即构建完整 Batch 3 流程，因为三个控制流都依赖尚未开发的 Batch 4/5 原子 Skill。当前只能构建诚实停止于缺失能力节点的控制流骨架。

---

# 1. 当前项目状态

## 1.1 已完成

### Batch 0：治理与评测基础

已具备：

- Skills registry；
- 系统架构；
- conflict matrix；
- quality-control plan；
- 状态与证据等级词表；
- deterministic checkers；
- DQE advisory evaluator；
- 基础测试与 shadow-run 机制。

### Batch 1：基础原子 Skill

已创建：

1. `documentation-quality-evaluator`
2. `project-state-reconstructor`
3. `goal-scope-and-workflow-elicitor`
4. `uncertainty-and-decision-manager`

### Batch 2：结构与证据 Skill

已创建并完成轻量首轮测试：

1. `workspace-forensics-and-inventory`
2. `document-information-architect`
3. `research-question-and-literature-planner`
4. `research-evidence-synthesizer`

共同状态：

```yaml
status: experimental
auto_trigger: false
disable_model_invocation: true
invocation: manual-only-or-orchestrator-only
```

## 1.2 暂未完成

- Batch 2 原子 Skill 之间的真实端到端接口验证；
- 多文档 corpus 模式；
- 真实 literature retrieval → evidence synthesis 链；
- Batch 3 控制流骨架；
- Batch 4/5 专业原子能力；
- 自动触发；
- DQE 通用 terminal-gate promotion。

---

# 2. 为什么不直接进入完整 Batch 3

Batch 3 包含三个控制流：

```text
numerical-research-software-design
scientific-workspace-reconstruction
documentation-refactor
```

但它们的完整调用链依赖大量尚未实现的原子 Skill。

## 2.1 数值设计流缺失能力

```text
research-software-problem-framer
scientific-software-architect
algorithm-technical-spec-author
scientific-prototype-experiment
scientific-validation-and-benchmark-planner
research-software-roadmap-author
```

## 2.2 工作区重建流缺失能力

```text
dev-test-experiment-workspace-architect
experiment-provenance-and-reproducibility
workspace-migration-planner
scientific-validation-and-benchmark-planner
living-design-maintainer
```

## 2.3 文档重构流缺失能力

```text
content-canonicalization-and-migration
technical-document-rewriter
living-design-maintainer
```

如果现在直接实现完整控制流，只会出现两种结果：

1. 控制流复制尚未存在的原子能力，破坏分层；
2. 控制流成为只有步骤列表、没有可执行接口的空壳。

因此，正确路线是：

> 先验证已有原子 Skill 的接口，再构建能在缺失节点诚实停止的控制流骨架。

---

# 3. Batch 2.5：集成冲刺

Batch 2.5 只运行两条真实链，不再扩张单体测试规模。

## 3.1 Track A：文档语料集成链

### 目标

一次性验证：

- `workspace-forensics-and-inventory` 的 document-corpus 模式；
- `project-state-reconstructor` 对文档语料事实的恢复；
- `goal-scope-and-workflow-elicitor` 的范围承接；
- `document-information-architect` 的多文档设计能力；
- Batch 1 与 Batch 2 的交接；
- 未来 `documentation-refactor` 的可运行前缀。

### 调用链

```text
workspace-forensics-and-inventory
  mode=document-corpus
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
→ documentation-quality-evaluator
  advisory only
→ independent reader
```

### 推荐测试对象

优先使用真实多文档语料：

- eoopt 混合路线图；
- 与其相关的质量报告；
- 决策记录；
- 测试报告；
- 状态文档；
- 或当前 `research-code-docs` 自身的治理与测试文档集合。

不要为此重新创建 synthetic corpus。

### 预期产物

```text
inventory-report.md
project-state-report.md
goal-scope-note.md
document-artifact-map.md
canonical-source-map.md
open-decisions.md
quality-advisory.md
```

### 验收条件

- 所有原始文档保持不变；
- forensics 不声称代码、测试或实验能够运行；
- state report 清楚区分 FACT、UNKNOWN、STALE、CANDIDATE；
- IA 为每种信息指定唯一 canonical home；
- 稳定设计与动态状态分离；
- volatile state 只通过 pointer 引用，不复制到稳定文档；
- 下游 Skill 不读取原聊天也能继续；
- 无法确定的归属进入 open decisions；
- IA 不移动、不重写、不删除文件；
- DQE 只提供 advisory report，不自动批准操作。

### 该链的长期用途

该链应保存为：

```text
documentation-refactor 的首个 integration fixture
```

## 3.2 Track B：真实研究证据链

### 目标

验证两个研究适配器是否能和真实 retrieval Skill 形成稳定交接。

### 调用链

```text
research-question-and-literature-planner
→ lit-review
→ research-evidence-synthesizer
→ uncertainty-and-decision-manager
→ documentation-quality-evaluator
  advisory only
```

### 研究范围限制

必须保持小规模：

```text
1 个明确研究问题
1 轮检索
5–8 个高相关来源
不追求完整综述
不调用大型 deep-research
```

可以继续使用此前的跨领域方法迁移问题，但必须由 `lit-review` 实际产生检索结果。

### RQLP → lit-review 验证

检查 search plan 是否包含：

- research questions；
- inclusion criteria；
- exclusion criteria；
- source priorities；
- stop criterion；
- evidence standard；
- transfer assumptions；
- routing rationale。

### lit-review → RES 验证

检查 RES 是否能消费真实 retrieval 结果：

- 每个来源是否可唯一识别；
- claim 是否可拆分；
- evidence channel 是否明确；
- source 内容不完整时是否保持 UNKNOWN；
- 是否能识别需要回退给 RQLP 的 evidence gaps；
- 是否避免把文献结论升级成项目事实。

### RES → decision manager 验证

检查：

- E0–E5 是否完整保留；
- paper/analogy evidence 不超过 E2；
- project evidence 独立记录；
- HYPOTHESIS、CANDIDATE、OPEN、DECIDED 不混淆；
- unresolved gaps 能进入 decision register；
- transfer assumptions 显式保留；
- decision manager 不把 evidence synthesis 自动变成用户决定。

---

# 4. OQ-4 暂不裁决

当前不合并：

```text
research-question-and-literature-planner
research-evidence-synthesizer
```

当前边界是：

```text
RQLP：检索前
RES：检索后
```

Batch 2.5 后仅评估：

1. lit-review 输出是否需要大量人工重排，RES 才能消费；
2. RQLP 与 RES 的中间 artifact 是否只是机械透传；
3. 两者的状态和 evidence 字段是否大量重复；
4. 合并是否会导致 planning 与 synthesis 再次越界混合。

只有在“接口成本显著高于边界收益”时才重新考虑合并。

---

# 5. Batch 2.5 最小接口冻结

这次不设计全系统复杂 schema，只冻结真实集成链需要的最小接口。

## 5.1 通用字段

每个中间 artifact 至少包含：

```yaml
artifact_type:
document_lifecycle:
produced_by_skill:
skill_version:
source_artifacts:
scope:
facts:
hypotheses:
open_questions:
evidence_level:
next_handoff:
handoff_requirements:
```

要求：

- 来源可追踪；
- 状态词一致；
- 下游能定位所需信息；
- 不依赖聊天上下文；
- 缺失信息不得默认为 false、done 或 verified；
- downstream requirements 必须显式；
- open questions 不得静默丢失。

## 5.2 首批冻结的接口

```text
inventory-report
project-state-report
goal-scope-note
document-artifact-map
literature-search-plan
research-evidence-map
decision-register
```

冻结的是：

- 字段；
- 字段语义；
- handoff 规则；
- required/optional 关系。

不冻结：

- Markdown 排版；
- 标题风格；
- 具体措辞；
- 非关键附加字段。

---

# 6. Batch 2.5 规模上限

必须保持轻量，防止重新进入 DQE 式测试扩张。

```text
真实集成链：2 条
每条主运行：1 次
每条定向重跑：最多 1 次
总 agent slots：不超过 12
不做三版本对照
不做每例三次稳定性
不新增大型 gold corpus
不恢复 Phase E
```

评价方式：

```text
deterministic interface checks
+
1 个独立 reader
+
DQE advisory report
+
人工复核关键边界
```

只有发现真实失败时，才新增 regression case。

---

# 7. Batch 2.5 退出条件

以下全部满足即可结束：

```text
两条真实链各完成一次主运行
所有源文件保持不变
每个下游 Skill 可仅依赖上游 artifact 继续
handoff 字段完整
状态词与 evidence level 保持一致
无 literature → project fact 升级
无 inventory → runtime fact 升级
无 IA 执行移动、改写或删除
无 RQLP 执行检索
无 RES 启动检索
所有发现的问题完成归类
```

问题分类必须是：

```text
SKILL_DEFECT
INTERFACE_DEFECT
MISSING_CAPABILITY
SOURCE_DATA_LIMITATION
TEST_HARNESS_DEFECT
```

Batch 2.5 完成后，四个 Batch 2 Skill 仍保持：

```yaml
status: experimental
auto_trigger: false
disable_model_invocation: true
```

不需要提升为 active。

---

# 8. 进入 Batch 3 前的架构修订

当前系统架构仍可能写成：

> DQE 是三个流程的 terminal gate；没有通过 DQE 就不能完成。

但 DQE 现在的正式定位是：

```text
advisory evaluator
profile-scoped
unsupported profile → INCOMPLETE
```

因此应将架构规则改为：

```text
DQE 是质量检查点，不是通用自动发布门。

在 supported profile 下：
  DQE advisory + human/orchestrator decision

在 unsupported profile 下：
  GATE_DECISION=INCOMPLETE
  流程转人工或未来专用能力

DQE ALLOW 不自动触发：
  发布
  文件移动
  文件删除
  文件覆盖
  Skill 安装
  auto-trigger 启用
```

这项架构一致性修订是 Batch 3 前唯一必需的治理修改。

---

# 9. Batch 3 开发顺序

## 9.1 第一：`documentation-refactor`

它拥有当前最完整的可运行前缀：

```text
workspace-forensics-and-inventory
  document-corpus mode
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
```

当前缺失能力：

```text
content-canonicalization-and-migration
technical-document-rewriter
living-design-maintainer
```

v0 骨架应在此处诚实停止。

## 9.2 第二：`scientific-workspace-reconstruction`

当前可运行前缀：

```text
workspace-forensics-and-inventory
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
```

随后应输出：

```text
flow_status=BLOCKED
blocked_by=dev-test-experiment-workspace-architect
```

不得临时在控制流中实现 workspace architecture 或 migration。

## 9.3 第三：`numerical-research-software-design`

当前可运行部分：

```text
project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ research-question-and-literature-planner
→ lit-review
→ research-evidence-synthesizer
→ uncertainty-and-decision-manager
```

但核心数值设计原子 Skill 尚未存在，因此暂时排第三。

---

# 10. Batch 3 v0 骨架职责

三个控制流只负责：

- 路由；
- 调用已有 Skill；
- 持久化中间 artifact；
- 管理用户决策点；
- 记录 flow state；
- 验证 handoff；
- 在能力缺失处停止；
- 输出下一步 handoff。

不得：

- 复制原子 Skill 写作规则；
- 临时实现 Batch 4/5 能力；
- 把未执行步骤标为完成；
- 自动移动、删除或覆盖文件；
- 自动运行两个 L1 flow；
- 把 DQE ALLOW 当作自动发布许可。

## 10.1 统一 flow-state 输出

```yaml
flow_name:
flow_version:
flow_status: RUNNING | BLOCKED | COMPLETE
current_stage:
completed_artifacts:
open_decisions:
blocked_by:
next_skill:
next_input:
quality_advisory:
source_commit:
```

当前 v0 骨架的大多数真实运行合理结果应是：

```text
flow_status=BLOCKED
blocked_by=missing-planned-capability
```

这不是失败，而是诚实的能力边界。

---

# 11. 当前真正的阻塞项

## 11.1 不阻塞下一阶段

以下事项不阻塞 Batch 2.5 或 Batch 3 骨架：

- DQE Phase E；
- controlled experiment release profile；
- Batch 2 auto-trigger；
- OQ-4；
- 第二个单体 shadow；
- 大型 admission matrix；
- DQE 通用 terminal-gate promotion。

## 11.2 阻塞完整 Batch 3 闭环

真正阻塞完整控制流的是尚未开发的原子能力。

### 数值设计

```text
research-software-problem-framer
scientific-software-architect
algorithm-technical-spec-author
scientific-prototype-experiment
scientific-validation-and-benchmark-planner
research-software-roadmap-author
```

### 工作区

```text
dev-test-experiment-workspace-architect
experiment-provenance-and-reproducibility
workspace-migration-planner
```

### 文档重构

```text
content-canonicalization-and-migration
technical-document-rewriter
living-design-maintainer
```

控制流骨架可以在这些能力缺失时存在，但不得宣称完整闭环。

---

# 12. 仓库卫生项

当前被跟踪的：

```text
make_grading_injection.cpython-312.pyc
```

应在下一提交中清理。

执行：

```text
删除 Git 跟踪中的 .pyc
将 __pycache__/ 加入 .gitignore
将 *.pyc 加入 .gitignore
确认没有其他被跟踪的编译缓存
```

这是一次性卫生修复，不是功能阻塞项。

---

# 13. 推荐 Sprint 计划

## Sprint 4：Batch 2.5 集成

```text
Track A：
forensics(document)
→ PSR
→ goals
→ IA
→ advisory review

Track B：
RQLP
→ lit-review
→ RES
→ decision register
→ advisory review

横切任务：
冻结最小 handoff schema
清理 .pyc
输出 integration report
```

### Sprint 4 产物

```text
docs/skill-development/reports/batch2_5-integration-2026-08-xx.md
references/interfaces/inventory-report.schema.md
references/interfaces/project-state-report.schema.md
references/interfaces/goal-scope-note.schema.md
references/interfaces/document-artifact-map.schema.md
references/interfaces/literature-search-plan.schema.md
references/interfaces/research-evidence-map.schema.md
references/interfaces/decision-register.schema.md
evals/skills/results/batch2_5/document-chain/
evals/skills/results/batch2_5/research-chain/
```

## Sprint 5：Batch 3 最小骨架

构建顺序：

```text
1. documentation-refactor
2. scientific-workspace-reconstruction
3. numerical-research-software-design
```

每个仅做：

```text
SKILL.md
flow-state template
routing/conflict cases
1 个前缀 e2e
1 个 missing-capability stop case
1 个 no-context reader test
```

不要求完整闭环。

---

# 14. 给本地 Agent 的执行提示词

```text
下一阶段执行 Batch 2.5 集成冲刺，不要直接构建完整 Batch 3。

目标：
验证 Batch 1–2 原子 Skill 的接口，而不是继续扩张单体测试。

Track A：
workspace-forensics-and-inventory(document-corpus)
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
→ DQE advisory
→ independent reader

使用真实多文档 corpus。
所有原文件必须保持不变。

Track B：
research-question-and-literature-planner
→ lit-review
→ research-evidence-synthesizer
→ uncertainty-and-decision-manager
→ DQE advisory

限制：
- 1 个明确问题
- 1 轮检索
- 5–8 个来源
- 不调用 deep-research
- 不追求完整综述

冻结最小接口：
- inventory-report
- project-state-report
- goal-scope-note
- document-artifact-map
- literature-search-plan
- research-evidence-map
- decision-register

每个接口至少包含：
artifact_type
document_lifecycle
produced_by_skill
skill_version
source_artifacts
scope
facts
hypotheses
open_questions
evidence_level
next_handoff
handoff_requirements

规模：
- 2 条链
- 每条主运行 1 次
- 每条最多定向重跑 1 次
- 总 agent slots <= 12
- 不做三版本对照
- 不做每例三次
- 不新增大型 corpus
- 不恢复 Phase E

退出条件：
- 两条链完成
- 原文件未修改
- 下游可脱离聊天消费上游 artifact
- 无事实升级
- 无边界越权
- 所有问题分类为 skill/interface/missing-capability/source-data/harness

完成 Batch 2.5 后：
1. 修订架构中 DQE terminal-gate 的旧表述；
2. 进入 Batch 3 最小骨架；
3. 顺序：
   documentation-refactor
   scientific-workspace-reconstruction
   numerical-research-software-design
4. 每个骨架必须在缺失原子能力处输出 BLOCKED，而不是假装完成。

同时清理被 Git 跟踪的 .pyc，并更新 .gitignore。
```

---

# 15. 最终决策

采用组合方案：

```text
先执行：
真实 RQLP → lit-review → RES 链
+
forensics corpus mode + IA 多文档模式

将二者合并为一个受限 Batch 2.5 集成冲刺。

通过后再执行：
Batch 3 三个最小控制流骨架。
```

核心原则：

> 先证明原子 Skill 能通过显式 artifact 接口组合，再建设编排层；控制流必须诚实记录缺失能力，不能用隐式上下文或临时逻辑掩盖尚未开发的原子 Skill。
