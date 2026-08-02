# DQE v4 待决策项回复与下一阶段开发计划

> 适用仓库：`ArmourPiercer1/research-code-docs`  
> 主要依据：
>
> - `docs/testing/decisions-pending-2026-07-31.md`
> - `docs/testing/adjudication-v4.md`
> - `docs/testing/corpus-repair-report-v4.md`
> - `docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md`
> - `docs/skill-development/reports/dqe-v0.4-defect-ledger.md`
>
> 被测 Skill：`documentation-quality-evaluator` v0.3.0  
> 当前语料：dataset version 4  
> 决策状态：本文对 D-6、D-7 给出最终建议，并规定后续 v0.4 Skill 开发与准入流程。  
> 日期：2026-07-31

---

## 0. 决策摘要

### D-6：选择 A，但对当前案例保留再利用价值

```text
DECISION_D6=A
```

执行含义：

1. 当前 `GN-PROP-001 v2` **不再作为 golden-negative**；
2. 不人工覆盖两位独立 reviewer 的 `PASS / ALLOW` 一致结论；
3. 将当前案例移入 quarantine，或改登记为非准入的 boundary/candidate 案例；
4. 使用一个更精简、受控的 technical proposal 基文档重建负例；
5. 新负例必须保证删除验证计划后，文档确实无法给出可验证的完成条件、测试方法或回退方案；
6. 新案例重新经过 mutation 语义校验和双盲审定，不继承旧 gold 标签。

理由：

- 两位隔离 reviewer 均以 HIGH confidence 判定当前变体仍可实现；
- v0.3 对它的 FAIL 来自 HF-9 profile 缺口和 mutation 残留矛盾，而不是目标缺陷；
- 人工将其覆盖为 FAIL 会把“语料预期”凌驾于实际文档可用性之上；
- 这会形成 evaluator 契约自证循环，并鼓励 DQE 对内容完整的外部提案过度阻断。

### D-7：选择 A，但必须采用 profile 限定后的窄规则

```text
DECISION_D7=A_QUALIFIED
```

锁定结果：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=BLOCK
REQUIRED_BLOCKERS=[HF-14b]
```

但 HF-14b 的 BLOCK 语义仅适用于以下条件全部成立的情形：

```text
provenance_policy = controlled
decision_mode = release-gate
artifact_type 属于稳定设计文档
该文档被声明为 canonical / BASELINE / ACCEPTED
正文写入未标日期的“当前”易变事实
没有指向唯一动态事实源
```

对于当前 `BP-002-fail v2`，上述条件成立，因此保留 `FAIL/BLOCK` 是合理的。

这不意味着“任何文档中出现一条测试数就自动硬失败”。下列情况不得因 HF-14b 自动 BLOCK：

- `external` 或 `legacy` 文档的普通 audit；
- 状态报告或实验报告本来就负责承载动态事实；
- 明确标注日期的冻结快照；
- 同时提供唯一动态状态源指针；
- 教学示例、历史数据或非 current claim；
- 易变事实仅出现在非 canonical 附录，且有明确更新机制。

---

# 1. 对 D-6 的正式回复

## 1.1 为什么不能选择 B：人工判 FAIL

当前 `GN-PROP-001 v2` 的基文档是 KEP-127。删除以下章节后：

- Test Plan；
- Graduation Criteria；
- Feature Enablement and Rollback；

文档仍然保留了足够丰富的：

- CRI protobuf 变更；
- ID 映射算法；
- worked examples；
- failure modes；
- alternatives；
- Production Readiness Review 内容；
- 详细实现约束。

两位 reviewer 均认为文档仍足以指导实现，并把缺失章节视为流程治理或成熟度管理内容，而不是阻止实现的必要条件。

因此：

> 当前案例没有成功隔离“技术提案不可执行”这一目标缺陷。

强行将它标记为 FAIL 会产生三个问题：

1. **破坏 gold 的独立性**  
   gold 将不再代表 reviewer 对文档真实质量的判断，而只是镜像 DQE 预设规则。

2. **训练错误严格度**  
   DQE 会被奖励为：只要外部 proposal 没有本项目偏好的 test/graduation 模板，就应 BLOCK。

3. **无法解释失败来源**  
   当前 v0.3 的失败原因是 HF-9 和附带矛盾，不是目标 finding，继续保留只会污染召回指标。

因此，不采用 D-6B。

## 1.2 为什么 A 优于 C

C 允许重新定义当前案例的目标缺陷，但这份文档已经被双 reviewer 判为无明显缺陷。如果为了继续保留负例而事后寻找另一种失败解释，仍有明显的数据后验定标风险。

推荐：

- 当前案例不作为 negative；
- 保留其内容和评审结果；
- 视情况转化为一个未来的 boundary case。

可选的新身份：

```yaml
case_id: BP-PROP-VALIDATION-SCAFFOLD-pass
class: boundary-pass
profile:
  provenance_policy: external
  decision_mode: audit
expected:
  quality_band: PASS
  gate_decision: ALLOW
required_findings:
  - implementation-details-remain-sufficient
notes:
  - missing formal graduation scaffolding alone does not make this external proposal non-executable
```

当前轮次也可以只 quarantine，不急于纳入 live corpus。

## 1.3 新 proposal 负例应如何重建

不建议继续随机寻找另一份大型 KEP。大型真实提案往往有大量冗余信息，删除一个章节未必能改变可执行性。

建议创建一组**受控、精简的 synthetic proposal pair**：

```text
GP-PROP-CONTROLLED-001
GN-PROP-VALIDATION-001
```

### 正例必须包括

```markdown
# Technical Proposal

## Problem
## Scope and non-goals
## Proposed design
## Interface changes
## Validation plan
## Acceptance criteria
## Rollout plan
## Rollback conditions
## Risks and mitigations
```

其中验证和门槛必须是 load-bearing 的，例如：

```text
Validation:
- Run benchmark A/B/C with fixed configurations.
- Compare numerical error and runtime against baseline v2.

Acceptance:
- Relative error ≤ 1e-5 on A and B.
- Runtime regression ≤ 10%.
- No failure on C.

Rollback:
- If any numerical invariant fails, retain the existing solver path.
```

### 负例只删除

- Validation plan；
- Acceptance criteria；
- Rollout/rollback conditions。

保留设计与接口说明，使其成为：

> 知道要实现什么，但不知道如何证明完成、如何安全发布或何时回退。

### 新负例的预期

```yaml
expected:
  quality_band: PARTIAL
  gate_decision: BLOCK
  document_quality: FAIL
  required_findings:
    - missing-validation-plan
    - no-verifiable-acceptance
    - missing-rollback
    - not-release-ready
  forbidden_blockers:
    - HF-9
    - HF-13
    - HF-14a
    - HF-14b
    - HF-15
```

暂时不要为此新增 hard gate。先测试 DQE 能否通过 proposal rubric 和 non-compensatory rule 给出 `BLOCK`。

若 DQE 稳定给出 `ALLOW`，再讨论：

- proposal 专用 hard gate；
- 或把 validation/release-readiness 设为 proposal 的非补偿维度。

## 1.4 D-6 的具体仓库操作

建议本地 Agent 执行：

```text
1. 将 tests/corpus/cases/golden-negative/GN-PROP-001/
   移至 tests/corpus/cases/quarantine/GN-PROP-001-v2/

2. QUARANTINE.yaml 中记录：
   reason: base-document-remains-executable-after-mutation
   reviewers: PASS/ALLOW, PASS/ALLOW
   original_intended_defect: missing-validation-story
   actual_dqe_failure: HF-9 + mutation-induced contradiction

3. 从 live manifest index 和 admission metrics 中排除旧案例。

4. 创建：
   tests/corpus/cases/golden-positive/GP-PROP-CONTROLLED-001/
   tests/corpus/cases/golden-negative/GN-PROP-VALIDATION-001/

5. 增加 mutation postconditions 和语义校验。

6. 重新运行 Reviewer A/B。
```

---

# 2. 对 D-7 的正式回复

## 2.1 为什么选择 BLOCK

`BP-002-fail v2` 不是普通外部文档，而是：

- `provenance_policy: controlled`；
- 稳定的 architecture document；
- 被声明为 BASELINE/ACCEPTED 设计；
- 在正文中写入“当前 69 项测试全部通过”；
- 没有时间戳；
- 没有指向动态状态 canonical source。

这条信息不是架构本身的一部分，其自然更新频率明显高于架构设计。把它复制进稳定 canonical 文档后，文档在第一次测试数变化时就会变成错误信息。

虽然只有一行，但它已经建立了一个错误的信息所有权：

```text
architecture.md 被读者误认为当前测试状态的事实源
```

终端 release gate 的职责不是只判断“读者能否理解架构”，还应阻止可预见、立即可修复且会造成漂移的 canonical-source 错误。

因此，合理结果是：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=BLOCK
```

这正是双轴 verdict 的用途：

- 文档整体并不差；
- 但在修复该行前不应作为受控 canonical 文档放行。

## 2.2 HF-14b 必须限定 applicability

HF-14b 不应继续表述为：

> 稳定文档中出现任何易变信息就硬失败。

建议写成：

### HF-14b BLOCK 条件

必须同时满足：

1. artifact 是稳定设计类型：
   - architecture；
   - roadmap；
   - ADR；
   - algorithm spec；
   - vision/baseline design；

2. evaluation profile 是：
   - `provenance_policy: controlled`；
   - `decision_mode: release-gate`；

3. 动态事实被写成 current claim：
   - “当前”；
   - “目前”；
   - “现有 N 项测试通过”；
   - “阶段已完成”；
   - 无日期的 active progress；

4. 未提供以下任一 escape hatch：
   - `as-of` 日期；
   - canonical dynamic source pointer；
   - 自动生成/update mechanism；
   - 明确标为历史快照；
   - 明确从属于 status appendix；

5. 该事实存在实际漂移风险或错误 ownership。

### 严重度映射

| Profile / mode | 处理 |
|---|---|
| controlled + release-gate | `HF-14b BLOCKER` |
| controlled + audit | `MAJOR`，默认不做发布决定 |
| legacy + audit | `MAJOR migration finding` |
| external + audit | `MINOR/MAJOR`，不因其单独 BLOCK |
| status/experiment report | 不适用 HF-14b |
| dated snapshot + pointer | PASS/escape |
| 同类动态值互相矛盾 | 转入 HF-14a |

## 2.3 D-7 的 manifest 锁定

保留：

```yaml
expected:
  document_quality: FAIL
  quality_band: PARTIAL
  gate_decision: BLOCK
  required_blockers: [HF-14b]
  forbidden_blockers: [HF-13, HF-14a, HF-15]
```

建议增加：

```yaml
profile:
  provenance_policy: controlled
  decision_mode: release-gate
```

当前 manifest 只有 `provenance_policy`，应补齐 `decision_mode`，使 BLOCK 的适用范围显式化。

## 2.4 增加相邻边界测试

仅靠当前 pass/fail pair 还不足以证明 severity mapping。

建议增加：

### `BP-002-audit`

同一份 fail 文档，profile 改为：

```yaml
provenance_policy: controlled
decision_mode: audit
```

预期：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=ALLOW 或 INCOMPLETE
HF-14b 不作为 release blocker
finding=volatile-in-stable
```

### `BP-002-external`

同一文档改为：

```yaml
provenance_policy: external
decision_mode: audit
```

预期：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=ALLOW
finding=volatile-in-stable
```

这样可以验证：

> BLOCK 来自受控 release-gate 契约，而不是模型对一行数字的机械惩罚。

---

# 3. 对当前测试修复结果的总体判定

测试修复轮是成功的。

修复后的 confirmatory spot-check 已证明：

- HF-15 召回正常；
- HF-12A 召回正常；
- HF-13/HF-14a 在干净 fixture 上没有复现此前的过度触发；
- 旧结果中的大部分 Skill 失败实际上来自 mutation 或 fixture；
- 唯一稳定复现的 Skill 缺陷是 HF-9 不识别 profile。

因此下一阶段不得继续修改：

```text
HF-12A
HF-15
HF-13 判别逻辑
HF-14a 判别逻辑
```

HF-13/HF-14a 可以补充契约文字与回归断言，但不应在缺少新失败证据时调整模型规则或 checker 阈值。

---

# 4. 下一阶段开发计划

下一阶段分为五个子阶段：

```text
A. 锁定 D-6/D-7 与 corpus
B. 接受 evaluator contract ADR
C. 实现 DQE v0.4 的最小 Skill 变更
D. 诊断矩阵与完整准入
E. 通过后解锁 Batch 2
```

---

## Phase A：完成决策与 corpus 收尾

### A1. 写回 D-6

在 `docs/testing/decisions-pending-2026-07-31.md` 中写入：

```text
D-6=A
GN-PROP-001 v2 quarantine
不得人工覆盖为 FAIL
重建 controlled lean proposal pair
```

### A2. 写回 D-7

写入：

```text
D-7=A_QUALIFIED
BP-002-fail v2:
QUALITY_BAND=PARTIAL
GATE_DECISION=BLOCK
HF-14b applies only under controlled + release-gate
```

### A3. 更新 corpus 状态

完成后应达到：

```text
disputed live cases = 0
invalid live cases = 0
quarantine cases 不进入 metrics
```

### A4. 重建 proposal pair

完成：

```text
GP-PROP-CONTROLLED-001
GN-PROP-VALIDATION-001
```

并通过：

```text
mutation postconditions
validate_mutation_semantics.py
validate_case_manifests.py
Reviewer A/B
```

Reviewer 对新负例至少应在 gate 轴达成：

```text
BLOCK / BLOCK
```

若再次得到 `ALLOW / ALLOW`，不得人工覆盖；应重新审视 proposal gate 的真实需求。

---

## Phase B：正式接受 ADR-DQE-001

将：

```text
status: PROPOSED
```

改为：

```text
status: ACCEPTED
```

但在接受前需要补充两个决定。

### B1. evaluation profile 如何进入 DQE

推荐采用：

> **terminal gate 调用时必须由 caller 显式传入 profile；DQE 不得静默推断 provenance 和 decision mode。**

调用契约：

```yaml
target: path/to/doc.md
evaluation_profile:
  artifact_type: architecture-doc
  provenance_policy: controlled
  decision_mode: release-gate
  evidence_requirement: key-claims
  reader_profile: architecture-comprehension
  output_mode: audit
```

当缺少 profile 时：

```text
允许执行一般 audit
不得发出最终 ALLOW
GATE_DECISION=INCOMPLETE
报告缺少的 profile 字段
```

可以推断 `artifact_type`，但不得静默推断：

```text
provenance_policy
decision_mode
```

原因：

- 它们决定 hard gate 严重度；
- 错误推断会再次制造 HF-9 类假失败；
- orchestrator 和 eval harness 已经能够显式提供 profile。

### B2. reproducibility 是否新增 hard gate

当前不新增 `HF-REPRO`。

理由：

- 修复后的 `GN-EXP-REPRO-001` 已被 v0.3 判为 BLOCK；
- 现阶段没有证据说明专属 hard gate 是必要的；
- 先观察 HF-9 profile 修复后，该案例是否仍由 HF-12A/E 或 non-compensatory rubric 正确阻断。

决策：

```text
OQ-REPRO=DEFER
```

仅在 v0.4 诊断矩阵中该案例错误 ALLOW 时，再设计专属 gate。

---

## Phase C：实现 DQE v0.4 最小变更

版本建议：

```text
documentation-quality-evaluator 0.4.0
```

### C1. 必须实现：profile-aware HF-9

修改：

```text
.claude/skills/documentation-quality-evaluator/SKILL.md
evals/skills/harness/hard-fail.md
evals/skills/harness/checkers/frontmatter_check.py
evals/skills/harness/make_grading_injection.py
scripts/make_eval_plan.py
evals/skills/harness/score_grading.py
scripts/aggregate_eval_results.py
```

要求：

1. checker 只输出 raw finding；
2. evaluator 根据 profile 映射严重度；
3. external/legacy 不因 HF-9 单独 BLOCK；
4. controlled release-gate 继续 BLOCK；
5. 输出回显实际使用的 profile；
6. profile 缺失时不允许 terminal ALLOW。

### C2. 必须实现：双轴 verdict

输出：

```text
QUALITY_BAND=<PASS|PARTIAL|FAIL>
GATE_DECISION=<ALLOW|BLOCK|INCOMPLETE>
DOCUMENT_QUALITY=<PASS|FAIL|INCOMPLETE_EVALUATION>
FACTUAL_VALIDITY=<VERIFIED|PARTIALLY_VERIFIED|UNVERIFIED>
READER_TEST=<PASS|FAIL>
CHECKER_STATUS=<COMPLETE|PARTIAL|NOT_RUN>
BLOCKERS=[...]
EVALUATION_PROFILE={...}
```

兼容映射：

```text
ALLOW      → DOCUMENT_QUALITY=PASS
BLOCK      → DOCUMENT_QUALITY=FAIL
INCOMPLETE → DOCUMENT_QUALITY=INCOMPLETE_EVALUATION
```

### C3. 必须实现：lifecycle vocabulary

将文档级状态改为：

```text
document_lifecycle:
DRAFT | IN_REVIEW | ACCEPTED | DEPRECATED
```

claim/decision status 保持原词表。

更新：

```text
status_vocab_check.py
frontmatter checker
templates
corpus manifests
DQE reader/evaluator instructions
```

过渡期可允许旧字段，但应输出 deprecation warning，不应把旧 `status: DECIDED` 自动解释为所有 claim 均已决定。

### C4. 只做契约澄清，不改变判别阈值

对于 HF-13/HF-14a：

- 将 ADR 中的精确定义同步到 `hard-fail.md`；
- 增加 regression tests；
- 不调整 checker 或 prompt 的实际严格度，除非诊断矩阵复现错误。

对于 HF-12A/HF-15：

```text
NO CHANGE
```

### C5. 同步 HF-14b 的 profile severity

实现 D-7 的限定规则：

```text
controlled + release-gate + stable canonical doc
+ bare current volatile fact + no pointer
→ HF-14b BLOCK

其他 profile/mode
→ finding / MAJOR / MINOR
```

这不是扩大 HF-14b，而是限定其 applicability。

---

## Phase D：诊断矩阵

Skill 修改后先运行小型诊断矩阵，不立即运行完整 admission。

### D1. 建议案例

| 类别 | 案例 | 重复 |
|---|---|---:|
| HF-9 profile | `BP-004-external` | 3 |
| HF-9 profile | `BP-004-controlled` | 3 |
| External experiment | `GP-EXP-001` | 3 |
| Reproducibility | `GN-EXP-REPRO-001` | 3 |
| Bare claim | `GN-EVIDENCE-BARE-CLAIM-001` | 3 |
| Roadmap | `GN-ROADMAP-001 v2` | 3 |
| Proposal | `GP-PROP-CONTROLLED-001` | 3 |
| Proposal | `GN-PROP-VALIDATION-001` | 3 |
| HF-14b release | `BP-002-fail v2` | 3 |
| HF-14b snapshot | `BP-002-pass` | 3 |
| HF-14b audit | `BP-002-audit` | 3 |
| Claim lifecycle | `BP-005-pass v2` | 3 |
| Unsupported verified | `BP-005-fail` | 3 |

建议总数：

```text
13 cases × 3 = 39 runs
```

### D2. 诊断通过条件

```text
BP-004 ordering = 100%
external docs 不因 HF-9 BLOCK
controlled missing frontmatter 触发 HF-9
BP-002 release case 3/3 BLOCK，仅 HF-14b
BP-002 pass case 3/3 ALLOW
BP-002 audit case 不因 HF-14b release rule BLOCK
BP-005 pass case 3/3 ALLOW
HF-12A、HF-15 回归 3/3 命中
proposal positive 3/3 ALLOW
proposal negative 3/3 BLOCK
forbidden blocker violation = 0
profile echo/schema validity = 100%
```

### D3. 何时允许进一步修改 Skill

只有在干净 fixture 上满足以下条件时：

```text
同一案例 3 次中至少 2 次出现同一错误
mutation semantic validation PASS
gold 无争议
不存在 secondary defect
```

才允许修改对应 gate。

---

## Phase E：完整准入矩阵

诊断通过后运行：

```text
with_dqe_v0.4
with_dqe_v0.3_frozen
without_skill
```

### E1. 完整指标

- false ALLOW on negative；
- false BLOCK on positive；
- required blocker recall；
- forbidden blocker violation；
- boundary ordering；
- profile compliance；
- gate-decision consistency；
- blocker-set Jaccard；
- score/quality-band stability；
- baseline gain；
- report cost与长度。

### E2. 稳定性规模

至少：

```text
5 cases × 3 runs
```

建议覆盖：

- external positive；
- controlled positive；
- roadmap negative；
- experiment/evidence negative；
- HF-14b boundary；
- proposal boundary。

### E3. provisional-gate 准入条件

```text
invalid/quarantined case 进入 live metrics = 0
unresolved gold dispute = 0
golden-negative false ALLOW = 0
golden-positive false BLOCK = 0
required blocker recall ≥ 0.90
forbidden blocker violation = 0
boundary ordering = 100%
profile compliance = 100%
5×3 gate-decision consistency = 100%
无 anchor regression
DQE 相对 without-skill 有明确增益
```

通过后状态：

```yaml
status: provisional-gate
disable-model-invocation: true
auto_trigger: false
terminal_gate_authority: limited
```

`limited` 表示：

- 可用于后续 Skill 输出的影子/人工准入；
- 关键 PASS 仍接受抽查；
- 不自动发布、不自动改写、不自动触发。

---

# 5. Batch 2 开发计划

只有 DQE 达到 `provisional-gate` 后，才解锁 Batch 2。

沿用现有系统路线：

## 5.1 `document-information-architect`

目标：

- 识别混合文档职责；
- 建立 artifact map；
- 分离 canonical source；
- 规划拆分、链接与生命周期；
- 输出 corpus information architecture。

首批测试应直接复用：

- hybrid roadmap；
- legitimate comprehensive report；
- stable/dynamic state boundary；
- external/legacy corpus。

## 5.2 `research-question-and-literature-planner`

定位为薄适配器：

- 把开放问题转成检索问题；
- 输出检索范围、关键词、证据标准；
- 路由到现有 `lit-review`、`wos-research` 或其他重型研究 Skill；
- 本身不虚构文献、不承担综合结论。

## 5.3 `research-evidence-synthesizer`

输入为已取得的证据，输出：

- claim→evidence matrix；
- direct/indirect/analogy/inference 标签；
- evidence level；
- transfer assumptions；
- unresolved gaps。

不得自行启动广泛检索，也不得把 E0–E2 写成 project-verified。

## 5.4 `workspace-forensics-and-inventory`

只读：

- 盘点代码、文档、实验、缓存和产物；
- 识别孤立脚本、未引用结果、重复状态源；
- 为 `project-state-reconstructor` 提供证据；
- 不移动、不删除、不重构。

该 Skill 还能持续提供真实测试语料，降低后续系统对 synthetic fixture 的依赖。

---

# 6. 建议提交顺序

建议拆成独立提交：

```text
test(dqe): resolve D6 and D7 decisions
test(corpus): quarantine invalid proposal negative
test(corpus): add controlled proposal boundary pair
docs(dqe): accept evaluation-profile ADR
feat(dqe): add explicit evaluation profile and profile-aware HF-9
feat(dqe): emit quality and gate verdict axes
refactor(dqe): separate document lifecycle from claim status
test(dqe): add HF-14b profile boundary cases
test(dqe): run v0.4 diagnostic matrix
test(dqe): run full admission and no-skill baseline
docs(dqe): record promotion decision
```

不要把 corpus 修复、Skill 行为修改和 admission 结果放在一个不可拆分的提交中。

---

# 7. 给本地 Agent 的执行提示词

```text
请根据本文件执行 DQE v4 后续开发。

已经裁决：

D-6=A：
- 当前 GN-PROP-001 v2 不再作为 golden-negative；
- 不允许人工覆盖两位 reviewer 的 PASS/ALLOW；
- quarantine 当前案例；
- 创建一个精简、受控的 proposal positive/negative pair；
- 新负例必须因缺少 validation、verifiable acceptance 和 rollback 而真实 BLOCK；
- 重新进行 mutation semantic validation 和 Reviewer A/B 双盲审定。

D-7=A_QUALIFIED：
- BP-002-fail v2 锁为 QUALITY_BAND=PARTIAL、GATE_DECISION=BLOCK；
- required blocker 为 HF-14b；
- BLOCK 只适用于 controlled + release-gate + stable canonical doc；
- external/legacy/audit、dated snapshot + pointer、status/experiment report 不得套用同一 BLOCK；
- 增加 audit/external 相邻边界测试。

执行顺序：

1. 写回 decisions-pending，并更新 defect ledger。
2. quarantine GN-PROP-001 v2，保证它不进入 live metrics。
3. 构建 GP-PROP-CONTROLLED-001 与 GN-PROP-VALIDATION-001。
4. 完成语义校验和双 reviewer 审定；不得用 DQE 生成 gold。
5. 更新并 ACCEPT ADR-DQE-001：
   - evaluation_profile 由 terminal-gate caller 显式传入；
   - profile 缺失时 GATE_DECISION=INCOMPLETE，不得静默 ALLOW；
   - 保持 QUALITY_BAND 与 GATE_DECISION 双轴；
   - document_lifecycle 与 claim status 分离；
   - 暂不新增 HF-REPRO。
6. 实现 DQE v0.4，修改范围限定为：
   - profile-aware HF-9；
   - 双轴 verdict；
   - lifecycle vocabulary；
   - HF-14b profile severity；
   - 必要的 schema、runner、scorer 支持。
7. 不修改 HF-12A、HF-15 的逻辑。
8. 不基于旧污染 fixture 修改 HF-13/HF-14a；只同步精确定义和回归测试。
9. 先运行 13 cases × 3 的诊断矩阵。
10. 诊断通过后再运行 v0.4 / frozen-v0.3 / without-skill 完整矩阵。
11. 只有满足本文准入条件，才将 DQE 提升为 provisional-gate 并解锁 Batch 2。

最终报告必须分别列出：
- corpus 变化；
- contract 变化；
- Skill 变化；
- 未修改项及理由；
- 诊断结果；
- baseline 增益；
- promotion 与 Batch-2 unlock 决定。
```

---

# 8. 最终状态目标

完成上述计划后的理想状态：

```text
D-6: RESOLVED — invalid negative quarantined and replaced
D-7: RESOLVED — qualified HF-14b release-gate rule accepted
ADR-DQE-001: ACCEPTED
DQE: v0.4.0
Corpus: no disputes, no invalid live fixtures
Diagnostic matrix: PASS
Full admission matrix: PASS
DQE status: provisional-gate
Batch 2: UNLOCKED
Auto-trigger: still disabled
```

核心原则：

> 不通过人工覆盖把无效负例变成 gold；也不因为一条规则需要严格，就让它脱离 profile 和使用场景无限扩张。
