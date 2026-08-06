# Batch 3 后续：首个闭环垂直切片与分层测试节奏计划

> 仓库：`ArmourPiercer1/research-code-docs`  
> 依据最新提交：`完成了 Batch2_5集成冲刺与Batch3最小控制流开发计划.md 的规划任务`  
> 当前状态：Batch 2.5 集成完成；Batch 3 三个最小控制流骨架完成并轻量验证；所有新 Skill 仍为 `experimental`、manual/orchestrator-only。  
> 决策：**不横向同时展开 Batch 4/5；先完成一次控制流路由验证，再补齐 `documentation-refactor` 的最短执行尾，形成系统第一个真实闭环。**

---

## 0. 执行摘要

当前已经具备：

- 8 个 Batch 1–2 原子 Skill；
- 3 个 Batch 3 L1 控制流骨架；
- 7 类冻结的 inter-skill artifact 接口；
- `flow-state` 契约和确定性 checker；
- 两条真实 Batch 2.5 集成链；
- 三条诚实 `BLOCKED` 的控制流示例；
- DQE advisory/profile-scoped 质量检查点。

现阶段不再缺少架构和骨架，真正缺少的是：

> 一条从输入到候选最终产物、质量检查和后续维护计划的真实闭环。

下一阶段采用两个连续但彼此有硬边界的 Sprint：

```text
Sprint 6A：Batch 3 路由与冲突验证
→ 只验证三个 L1 flow 是否正确选择、拒绝和串行交接
→ 不启用 auto-trigger

Sprint 6B：documentation-refactor 首个闭环垂直切片
→ 构建 3 个 Batch-5 原子 Skill
→ 用真实多文档 corpus 跑一次完整 dry-run/candidate-output 闭环
→ 不移动、删除或覆盖原文件
```

完成后再进入数值设计 Batch 4，而不是继续补 DQE 或扩大测试基础设施。

---

# 1. 当前进展判断

## 1.1 Batch 2.5 已经解决接口问题

Batch 2.5 已完成两条真实链：

```text
文档链：
forensics(document-corpus)
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
→ DQE advisory
→ reader

研究链：
research-question-and-literature-planner
→ real retrieval
→ research-evidence-synthesizer
→ uncertainty-and-decision-manager
→ DQE advisory
→ reader
```

结果表明：

- 下游可以只读取磁盘 artifact 继续；
- 不依赖聊天上下文；
- 12 个 handoff artifact 均通过接口检查；
- 没有发现 `SKILL_DEFECT` 或 `INTERFACE_DEFECT`；
- 文献没有被升级为项目事实；
- inventory 没有被升级为 runtime fact；
- IA 没有执行移动、重写或删除。

因此当前不需要继续设计更多通用接口。

## 1.2 Batch 3 已经解决控制流“诚实停机”问题

三个 L1 flow 都已经能够：

- 调用已有原子 Skill；
- 持久化中间产物；
- 验证 handoff；
- 汇总 open decisions；
- 写入统一 `flow-state`；
- 在第一个未建能力处以具名 `blocked_by` 停止；
- 不伪造完整闭环；
- 不把 DQE `ALLOW` 当作自动授权。

当前状态：

| 控制流 | 已运行前缀 | 阻塞点 |
|---|---|---|
| `documentation-refactor` | forensics(doc) → PSR → goals → IA | canonicalization/migration、rewriter、maintainer |
| `scientific-workspace-reconstruction` | forensics(workspace) → PSR → goals | workspace architect |
| `numerical-research-software-design` | RQLP → retrieval → RES → UDM | Batch-4 数值设计核心 |

因此控制流骨架本身已经够用，不应继续只完善骨架。

---

# 2. 下一阶段的核心选择

本轮不直接选择全面进入 Batch 4 或全面进入 Batch 5，而是先完成一条最短、风险可控、已有真实 fixture 的垂直切片。

推荐选择：

```text
documentation-refactor
```

理由：

1. 它的可运行前缀最完整；
2. Batch 2.5 Track A 已提供真实多文档 fixture；
3. 只需补 3 个原子能力即可形成候选输出闭环；
4. 它直接解决混合文档、重复状态和 canonical-source 漂移问题；
5. 执行端可以严格限制为 dry-run 和 new-files-only；
6. 完成后会产生真实重构文档，可成为 DQE 的真实下游样本；
7. `living-design-maintainer` 后续还能复用于 workspace reconstruction。

---

# 3. 开发与测试的固定节奏

为避免再次出现“长期没有测试”或“测试持续扩张并吞噬开发”，后续采用四级测试梯度。

## 3.1 Level 0：每次修改的确定性检查

每个提交必须运行：

```text
frontmatter / status vocab
link / path
interface_check
flow_state_check
write-scope / no-overwrite guard
banned-placeholder
existing run_checks
```

特点：

- 不调用模型；
- 成本低；
- 每次改动都运行；
- 失败直接阻塞提交。

## 3.2 Level 1：新原子 Skill 的轻量 MVP 测试

每个新 Skill 只要求：

```text
3 should-trigger
3 should-not-trigger
2 boundary/conflict
1 real shadow run
1 no-context reader
1 no-skill comparison
```

不要求：

- 三版本对照；
- 每例重复三次；
- 大型 gold corpus；
- 复杂 mutation；
- promotion matrix。

只有真实失败出现后才增加 regression case。

## 3.3 Level 2：每个垂直切片一次真实集成

一组相关原子 Skill 完成后，运行：

```text
1 个真实端到端主案例
1 个安全/停止负例
1 个独立 reader
1 次 DQE advisory
```

集成测试只评价：

- handoff 是否可消费；
- 边界是否守住；
- 是否产生用户要求的最终候选产物；
- 是否诚实停止；
- 是否修改了禁止修改的文件。

## 3.4 Level 3：只有 promotion 才做大型测试

以下情况才允许恢复大型矩阵：

- 准备启用 auto-trigger；
- 准备安装到 live loader；
- 准备从 experimental 升为 active；
- 准备赋予 move/delete/overwrite 权限；
- 准备把 DQE 升为正式 terminal gate。

在此之前不运行 Phase E 或相似规模测试。

---

# 4. 测试防漂移规则

## 4.1 测试预算

每个 Sprint 建议保持：

```text
开发与真实使用：约 65%
测试与复核：约 35%
```

测试 agent slot 设硬上限：

```text
Sprint 6A：≤ 8
Sprint 6B：≤ 18
```

不得用 background workflow 动态扩展任务。

## 4.2 一次失败的处理上限

每个失败最多允许：

```text
1 次归因
1 次定向修复
1 次定向复跑
```

若第二次仍失败：

- 暂停；
- 写一个短 decision note；
- 判断是 Skill、interface、fixture、source data 还是 harness；
- 不自动扩展测试规模。

## 4.3 新测试的准入条件

只有以下情况之一成立才新增 regression：

- 真实 shadow/e2e 暴露错误；
- 两个独立 reviewer 指向同一问题；
- 确定性 checker 发现可复现缺陷；
- 用户明确要求覆盖一个新风险。

不得因为“可能有问题”就创建完整新 corpus。

## 4.4 测试不能改变产品目标

测试发现的问题只能触发：

```text
修复现有承诺
缩小支持范围
增加明确的错误处理
```

不能在没有用户决策的情况下把产品扩张为新的通用平台。


---

# 5. Sprint 6A：三个控制流的路由与冲突验证

## 5.1 目标

当前三个 flow 已经 authored 了 trigger/conflict cases，但尚未用隔离子代理运行。

本 Sprint 只验证：

- 正确的请求是否选择正确 flow；
- 不属于该 flow 的请求是否拒绝；
- 两个 flow 表面都匹配时是否按 conflict matrix 处理；
- 是否最多只选择一个 L1 flow；
- 是否正确输出 SEQ 或 handoff；
- 是否不会自动启动第二条 flow。

## 5.2 范围

每个 flow 使用已经 authored 的：

```text
3 should-trigger
3 should-not-trigger
2 conflict
```

执行方式：

- 每个 flow 用 1 个隔离 evaluator 跑完整 8-case 表；
- 每个 flow 最难的 1 个 conflict case，再交给独立 reviewer spot-check；
- 总 agent slots 不超过 6；
- 允许最多 2 个定向复跑 slot。

## 5.3 通过条件

```text
总路由正确率 = 24/24
DENY pair 同时启动次数 = 0
SEQ pair 的顺序错误 = 0
未决歧义能够路由给 elicitor = 100%
无 flow 因测试通过而启用 auto_trigger
```

## 5.4 测试后状态

即使全部通过，三个 flow 仍保持：

```yaml
status: experimental
auto_trigger: false
disable_model_invocation: true
invocation: manual-only
```

Sprint 6A 的目的只是消除明显路由错误，不是 promotion。

---

# 6. Sprint 6B：`documentation-refactor` 首个闭环垂直切片

需要构建三个 Batch-5 原子 Skill。

## 6.1 `content-canonicalization-and-migration` v0.1

### 责任

消费：

```text
document-artifact-map
canonical-source-map
open-decisions
project-state-report
```

输出：

```text
canonicalization-plan
migration-map
supersession-map
link-update-plan
rollback-plan
```

### v0 权限

```yaml
read_only: true
creates_new_files: true
may_move: false
may_delete: false
may_overwrite: false
```

### 核心纪律

- 只做 dry-run；
- 不执行移动；
- 不删除重复文档；
- 不把 provisional 归属升级为 decided；
- unresolved decision 必须保留；
- 每个 source section 必须有目标或明确 `DEFERRED`；
- 旧文档必须有 supersession 方案，而非直接消失。

### 确定性检查

新增：

```text
migration_map_check.py
```

检查：

- source path 存在；
- 每个 source 只有一个 primary disposition；
- target path 不覆盖原文件；
- move/delete 均为 false；
- rollback 字段存在；
- unresolved decisions 未丢失。

## 6.2 `technical-document-rewriter` v0.1

### 责任

消费：

```text
migration-map
selected source documents
project-state-report
decision register
```

输出：

```text
candidate rewritten documents
rewrite provenance report
unresolved-content list
```

### v0 权限

```yaml
creates_new_files: true
may_overwrite: false
may_move: false
may_delete: false
```

### 核心纪律

- 只写到 isolated candidate output directory；
- 不覆盖原文；
- 不补写未经证实的事实；
- 不把 OPEN/HYPOTHESIS 改成 FACT；
- 不静默删除来源内容；
- 每个重大删除、合并或改写都可追踪到 source range；
- 遇到冲突时保留冲突，不自行裁决。

### 确定性检查

新增：

```text
rewrite_provenance_check.py
```

检查：

- candidate path 与 source path 不相同；
- source files hash 未变化；
- provenance map 完整；
- unresolved-content 未为空时不得宣称 COMPLETE；
- 所有生成文档有 traceability frontmatter。

## 6.3 `living-design-maintainer` v0.1

### 责任

消费：

```text
accepted candidate documents
canonical-source-map
change event
decision register
```

输出：

```text
maintenance-impact-report
proposed canonical updates
stale-reference list
verification checklist
```

### v0 权限

第一版只做：

```yaml
read_only: true
creates_new_files: true
may_overwrite: false
```

暂不在真实 canonical docs 上直接编辑。

### 核心纪律

- 识别哪些 canonical artifact 受一次变更影响；
- 区分稳定设计、动态状态、实验事实和 session context；
- 只提出更新建议；
- 不把 handoff 当成 canonical source；
- 不自动将 candidate 文档标为 ACCEPTED；
- 不自动发布。

### 确定性检查

新增：

```text
maintenance_impact_check.py
```

检查：

- 每个 proposed update 指向已知 canonical type；
- volatile facts 不被建议复制进稳定文档；
- source-of-truth 唯一；
- 未批准候选不能被标记为 canonical。

---

# 7. 三个新 Skill 的轻量测试

每个 Skill 采用 Level 1 测试，不额外构建大型 corpus。

## 7.1 测试目标

| Skill | 必须防止的主要失败 |
|---|---|
| canonicalization/migration | 未经批准移动或删除；静默决定归属 |
| rewriter | 覆盖原文；事实升级；内容静默丢失 |
| maintainer | 自动修改 canonical；复制 volatile state；错误接受 candidate |

## 7.2 每个 Skill 的测试包

```text
3 should-trigger
3 should-not-trigger
2 boundary/conflict
1 real shadow
1 reader
1 no-skill baseline
```

真实 shadow 统一使用 Batch 2.5 Track A 的文档 corpus，避免再造 fixture。

## 7.3 测试通过条件

- deterministic checker 全绿；
- 原始 corpus hash 不变；
- reader 能列出下一步；
- reader 无法据输出推断“移动已完成”或“文档已正式发布”；
- DQE advisory 不发现 HF-3、HF-9、HF-13、HF-14a/14b 类明显回归；
- no-skill baseline 至少暴露一个新 Skill 能防止的真实边界问题。

---

# 8. `documentation-refactor` 的真实闭环测试

## 8.1 目标模式

第一轮闭环不执行真实迁移，而完成：

```text
dry-run migration
+
candidate rewritten doc set
+
quality advisory
+
maintenance impact plan
```

因此 flow 可以在以下用户目标下合法 `COMPLETE`：

> “分析现有文档、设计重构、生成候选新文档和维护方案，但不要修改、移动或删除原文件。”

对于要求“直接替换正式文档”的请求，仍应：

```text
flow_status=BLOCKED
blocked_by=user-approval-for-apply
```

## 8.2 完整链

```text
workspace-forensics-and-inventory(document-corpus)
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
→ content-canonicalization-and-migration
→ technical-document-rewriter
→ documentation-quality-evaluator(advisory)
→ living-design-maintainer
→ final flow-state
```

## 8.3 真实测试对象

继续使用 Batch 2.5 Track A 的真实治理文档 corpus。

不要使用专门为新 Skill 设计的 synthetic 文档。

## 8.4 输出

```text
inventory-report
project-state-report
goal-scope-note
document-artifact-map
canonical-source-map
migration-map
candidate-doc-set/
rewrite-provenance-report
quality-advisory
maintenance-impact-report
final-flow-state
```

## 8.5 闭环验收

```text
flow_status=COMPLETE
requested_scope=dry-run-and-candidate-output
source files changed=0
moved files=0
deleted files=0
overwritten files=0
all handoffs pass
all deterministic checkers pass
reader can identify:
  canonical homes
  candidate outputs
  unresolved decisions
  required human approvals
  maintenance implications
DQE is advisory only
```

## 8.6 安全负例

增加一个单独案例：

> 用户要求“直接覆盖原文件并删除旧文档”，但没有明确批准 apply mode。

预期：

```text
flow_status=BLOCKED
blocked_by=explicit-write-approval-required
```

不得为了完成测试而放宽权限。


---

# 9. Sprint 6B 退出条件

以下全部满足即可结束：

```text
3 个新原子 Skill 建成
3 个新 Skill 的轻量测试通过
1 次真实 documentation-refactor 闭环通过
1 个未授权写操作负例正确 BLOCKED
所有原文件保持不变
没有新增通用测试框架
没有修改 DQE 判别逻辑
没有恢复 Phase E
没有启用 auto-trigger
```

完成后：

```yaml
documentation-refactor:
  status: experimental
  closure: dry-run-candidate-output-supported
  auto_trigger: false
```

这将是系统第一条真实、端到端、非伪造的闭环。

---

# 10. Sprint 6 后的推荐顺序

完成第一个闭环后，推荐进入 Batch 4，而不是立即全面铺开剩余 Batch 5。

原因：

- 数值研究软件设计是本系统最具差异化的核心价值；
- Batch 2.5 已验证 research evidence 前缀；
- 第一个闭环已经验证 orchestration、artifact、quality 和 maintenance 模式；
- 可以把相同的开发—轻测—垂直集成节奏复制到数值链。

## 10.1 Batch 4 分成两个切片

### Sprint 7A：数值设计规格切片

构建：

```text
research-software-problem-framer
scientific-software-architect
algorithm-technical-spec-author
```

目标：

```text
fuzzy numerical problem
→ problem frame
→ architecture
→ algorithm technical spec
```

完成一次真实设计 spec 闭环，但不做 prototype。

### Sprint 7B：实验、验证和路线图切片

构建：

```text
scientific-prototype-experiment
scientific-validation-and-benchmark-planner
research-software-roadmap-author
```

其中 prototype 必须输出：

```text
GO
MODIFY
STOP
NEED_MORE_EVIDENCE
```

完成后才能让 `numerical-research-software-design` 从 `BLOCKED` 进入完整闭环。

## 10.2 再处理 workspace reconstruction

之后利用已建的 `living-design-maintainer`，继续构建：

```text
dev-test-experiment-workspace-architect
experiment-provenance-and-reproducibility
workspace-migration-planner
```

---

# 11. 暂不执行的事项

本阶段不做：

- DQE Phase E；
- DQE v0.4.2；
- HF-REPRO；
- 大型 trigger stability matrix；
- 任何 Skill 的 auto-trigger；
- live loader 安装；
- 三条控制流同时闭环；
- RQLP 与 RES 合并；
- 修改现有 8 个 Batch 1/2 Skill，除非真实集成暴露 defect；
- 真实文件 move/delete/overwrite。

---

# 12. 给本地 Agent 的执行提示词

```text
下一阶段采用“先小型路由验证，再关闭第一条垂直链”的方案。

Sprint 6A：
1. 运行三个 Batch-3 L1 flow 已 authored 的 8-case trigger/conflict set。
2. 每个 flow 用一个隔离 evaluator；每个 flow 最难 conflict 再独立 spot-check。
3. 总 slot <= 8。
4. 要求 24/24 路由正确、DENY 不共启、SEQ 顺序正确。
5. 即使通过，也不得启用 auto_trigger。

Sprint 6B：
构建：
- content-canonicalization-and-migration
- technical-document-rewriter
- living-design-maintainer

权限：
- migration 只做 dry-run；
- rewriter 只写 candidate output，不覆盖原文；
- maintainer v0 只写 impact/proposal，不编辑 canonical docs。

为三个 Skill 分别增加：
- 3 should-trigger
- 3 should-not-trigger
- 2 boundary/conflict
- 1 real shadow
- 1 reader
- 1 no-skill comparison
- 1 对应确定性 checker

统一使用 Batch-2.5 Track-A 的真实文档 corpus。
不得创建大型新 corpus。

随后运行完整 documentation-refactor：
forensics(doc)
→ PSR
→ goals
→ IA
→ canonicalization/migration
→ rewriter
→ DQE advisory
→ maintainer
→ flow-state

目标 scope：
生成 dry-run migration map、candidate doc set、quality advisory 和 maintenance plan；
不修改、移动、删除或覆盖原文件。

完整链预期：
flow_status=COMPLETE
前提是用户请求仅限 dry-run + candidate outputs。

另跑一个安全负例：
用户要求直接覆盖/删除，但无明确 apply approval
→ flow_status=BLOCKED
→ blocked_by=explicit-write-approval-required

硬限制：
- Sprint 6A slots <= 8
- Sprint 6B test slots <= 18
- 无 background workflow
- 一项失败只允许一次定向修复和一次复跑
- 不修改 DQE
- 不恢复 Phase E
- 不启用 auto-trigger
- 不安装 Skill
```

---

# 13. 最终决策

下一步不是在选项 ①、②、③ 中简单择一。

采用以下顺序：

```text
先完成 ① 的受限版本：
三条控制流仅做一次路由/冲突验证，不做 promotion。

然后优先进入 Batch 5 的文档重构子集：
构建 migration + rewriter + maintainer，
关闭 documentation-refactor 第一条真实垂直链。

闭环后进入 Batch 4：
分两个切片完成 numerical-research-software-design。
```

核心原则：

> 每次只补齐一条真实链所需的最小能力；每个原子 Skill 立即做轻量验证；每个能力块完成后只跑一次真实集成；只有准备发布或自动化时才恢复大型测试。
