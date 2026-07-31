# Documentation Quality Evaluator：测试体系修正、最小升级与二阶段准入计划

> 适用仓库：`ArmourPiercer1/research-code-docs`  
> 基线提交：`279c0ce6904f24f0fa297b1f4c7abd637778d1d0`  
> 被测 Skill：`documentation-quality-evaluator` v0.3.0  
> 依据报告：`docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md`  
> 文档状态：`DECIDED — 作为 v0.4 前的修正与复测执行计划`  
> 最后更新：2026-07-31

---

## 0. 执行结论

当前盲测结果不能简单归因为“测试缺陷与 Skill 缺陷各占一半”。

更准确的判断是：

1. **测试语料、mutation 与 gold 契约存在多项明确缺陷，当前占主要影响；**
2. **DQE 本身存在两个已经被较干净证据支持的问题：**
   - HF-9 不识别 `external / legacy / controlled` profile；
   - HF-13 与 HF-14a 存在过度触发或误分类；
3. **另有若干系统契约尚未定义：**
   - evaluation profile 如何进入 DQE；
   - 文档生命周期状态与 claim/decision 状态如何区分；
   - “文档整体质量”与“是否允许放行”是否继续共用一个二元 verdict；
   - 实验可复现性应由哪一条专属规则评价；
4. `GN-EXP-001` 与 `GN-ROADMAP-001` 尚不能证明 HF-12A 和 HF-15 存在真实召回缺陷，因为对应 mutation 未将目标缺陷干净做实；
5. **进入 Batch 2 前，不应全面强化 DQE，也不应按当前 7 项红色指标直接调参。**

推荐顺序：

```text
冻结当前 v0.3 基线
→ 明确 evaluator 输入/输出契约
→ 隔离并修复无效 fixtures
→ 重新审定 gold 标签
→ 只修改 HF-9、HF-13、HF-14a
→ 运行小型诊断矩阵
→ 必要时再修改 HF-12A/HF-15
→ 运行完整盲测准入矩阵
→ 决定是否解锁 Batch 2
```

在完成本计划前，DQE 保持：

```yaml
status: experimental
invocation: manual-orchestrator-only
terminal_gate_authority: false
auto_trigger: false
```

---

## 1. 本轮目标与非目标

### 1.1 目标

本轮需要完成：

- 修复评测输入输出契约中的歧义；
- 清理无效、污染或弱 mutation 测试案例；
- 重新建立可归因的 boundary pair 与 golden-negative；
- 对 DQE 进行最小范围升级；
- 建立“小型诊断矩阵 → 完整准入矩阵”的两阶段复测流程；
- 给出明确、可机器检查的 Batch 2 解锁条件。

### 1.2 非目标

本轮暂不做：

- 不全面重写 DQE；
- 不将所有 soft finding 升级为 hard fail；
- 不因为当前漏判直接加强 HF-12A 或 HF-15；
- 不新增自动触发；
- 不发布 Skill；
- 不进入 Batch 2 的正式 Skill 创建；
- 不把 evaluator 自己的 verdict 反向写成 gold label；
- 不将 `PARTIAL` 与 `BLOCK` 的语义继续混为一谈。

---

## 2. 本次盲测的关键事实

当前盲测矩阵包括：

- 20 个 current case；
- 6 个 repeat run；
- 26/26 运行成功；
- 0 运行时错误；
- schema 输出合法；
- checker 均完成。

聚合结果显示 7 项准入指标全部未达标，但逐案核查后发现，聚合指标混合了三类原因：

```text
A. 测试案例没有真正承载目标缺陷
B. gold / forbidden blocker 契约本身不合理
C. DQE 真实判别缺陷
```

因此，当前指标只能证明：

> v0.3 尚不能提升为正式准入门。

当前指标不能直接证明：

> HF-12A、HF-15、HF-13、HF-14a 都应同时加强。

---

## 3. 失败项重新归因

## 3.1 明确属于测试或语料的问题

| 案例 | 发现 | 归因 | 当前处置 |
|---|---|---|---|
| `GN-EXP-001` | 删除 commit/环境后，仍保留训练命令、数据流程、完整超参数、LR schedule 和输出说明 | mutation 过弱；HF-12A 目标不纯 | quarantine，重做 |
| `GN-ROADMAP-001` | 注入“届时定”后仍保留 `GO: ≥20%` 和 downstream route | mutation 失败，目标缺陷未成立 | quarantine，重做 |
| `BP-002-fail` | `DECIDED`、`The core is done` 与 `design review in progress` 共存 | fixture 自身有真实状态矛盾 | 清理 fixture 或允许 HF-14a |
| `BP-005-pass` | 正文明示 HYPOTHESIS，但 frontmatter 写 `status: DECIDED` | metadata schema 歧义 | 改 schema 后重做 |
| `GN-PROP-001` | 删除章节后保留悬空 TOC 条目 | mutation 引入二次缺陷 | 清理 TOC 并重审 |
| 单一 PASS/FAIL gold | reviewer 认为 PARTIAL，但 gate 契约要求 FAIL | quality 与 gate decision 混用 | 拆成双轴标签 |

## 3.2 明确属于 Skill 的问题

| 问题 | 证据 | 结论 |
|---|---|---|
| HF-9 不识别 profile | 同字节 ADR 在 external 与 controlled profile 下应有不同判定，但 v0.3 无 profile 输入契约 | 必须新增 profile-aware 行为 |
| HF-13 过度触发 | 单一 architecture doc 加一段 maturity snapshot 被判为混合职责 | 需收紧触发条件 |
| HF-14a 误分类 | 悬空 TOC、metadata 歧义被解释为状态矛盾 | 需限制为同一状态变量的矛盾断言 |
| profile 行为不稳定 | external 文档多次运行出现 PASS/FAIL 波动 | profile 必须成为显式输入而非隐式推断 |

## 3.3 尚不能归因给 Skill 的问题

以下两项暂不修改 Skill：

- HF-12A 在 `GN-EXP-001` 上的漏判；
- HF-15 在 `GN-ROADMAP-001` 上的漏判。

只有在修复后的 fixture 真正满足预期缺陷，且 DQE 重复运行仍稳定漏判时，才将其升级为 Skill 缺陷。

---

## 4. 第一阶段：冻结基线并建立变更边界

### 4.1 冻结当前状态

创建 tag 或分支：

```bash
git tag dqe-v0.3-blind-matrix-baseline 279c0ce6904f24f0fa297b1f4c7abd637778d1d0
git switch -c dqe/v0.4-contract-corpus-fix
```

保存以下文件不覆盖：

```text
.claude/skills/documentation-quality-evaluator/SKILL.md
evals/skills/harness/hard-fail.md
evals/skills/harness/rubric.md
evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/
tests/corpus/blind-runs/matrix-2026-07-31/
docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md
```

### 4.2 建立缺陷账本

新增：

```text
docs/skill-development/reports/dqe-v0.4-defect-ledger.md
```

每项缺陷至少记录：

```yaml
id:
category: skill | fixture | contract | harness
evidence:
affected_cases:
decision:
planned_change:
regression_cases:
status: OPEN | IMPLEMENTED | VERIFIED | REJECTED
```

---

## 5. 第二阶段：先修 evaluator 契约

在修改 hard gates 前，先创建 ADR：

```text
docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md
```

## 5.1 新增显式 evaluation profile

DQE 输入契约至少应包括：

```yaml
target: path/to/document.md

evaluation_profile:
  artifact_type: adr | roadmap | architecture-doc | experiment-report | ...
  provenance_policy: controlled | legacy | external
  decision_mode: release-gate | audit
  evidence_requirement: full | key-claims | labeled-only | none
  reader_profile: adr-comprehension | roadmap-execution | ...
  output_mode: gate | audit
```

### provenance_policy 语义

#### `controlled`

适用于：

- 本 Skills 系统生成的正式文档；
- 已声明遵循本地规范的项目文档；
- 发布或合并准入。

规则：

```text
缺少本地 traceability metadata → HF-9 BLOCKER
```

#### `legacy`

适用于：

- 历史工作区文档；
- 尚未迁移到本地规范的文档；
- 文档重构输入。

规则：

```text
缺少本地 metadata → migration finding / MAJOR
除非调用方明确要求按 controlled gate 检查
```

#### `external`

适用于：

- GitHub 上游文档；
- 论文附带说明；
- 外部标准、RFC、PEP、KEP、ADR。

规则：

```text
缺少本地 traceability metadata → MINOR 或 N/A
不得仅因 HF-9 判 FAIL
```

## 5.2 拆分文档生命周期与认识状态

废弃歧义字段：

```yaml
status: DECIDED
```

改为：

```yaml
document_lifecycle: DRAFT | IN_REVIEW | ACCEPTED | DEPRECATED
```

正文或 register 中的 claim/decision 状态继续使用：

```text
FACT
VERIFIED
DECIDED
BASELINE
HYPOTHESIS
CANDIDATE
OPEN
DEFERRED
REJECTED
STALE
```

规则：

- `document_lifecycle` 描述文档本身是否草稿、评审中或已接受；
- claim status 描述具体主张的知识状态；
- 一份 `ACCEPTED` 的 evidence note 可以包含 `HYPOTHESIS`；
- “文档已接受”不等于“文档中所有主张已验证”。

## 5.3 拆分质量评价与放行决定

推荐输出：

```text
QUALITY_BAND=<PASS|PARTIAL|FAIL>
GATE_DECISION=<ALLOW|BLOCK|INCOMPLETE>
FACTUAL_VALIDITY=<VERIFIED|PARTIALLY_VERIFIED|UNVERIFIED>
READER_TEST=<PASS|FAIL>
CHECKER_STATUS=<COMPLETE|PARTIAL|NOT_RUN>
BLOCKERS=[...]
```

语义：

- `QUALITY_BAND`：整体文档质量；
- `GATE_DECISION`：当前工作流是否允许继续；
- `BLOCKERS`：导致 BLOCK 的未解决问题；
- `FACTUAL_VALIDITY`：事实或来源核验程度。

例如：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=BLOCK
BLOCKERS=[HF-15]
```

表示：

> 文档整体大部分合格，但存在一个阻止放行的硬性问题。

### 兼容策略

v0.4 可暂时保留：

```text
DOCUMENT_QUALITY=<PASS|FAIL|INCOMPLETE_EVALUATION>
```

但应将它定义为：

```text
DOCUMENT_QUALITY = GATE_DECISION 的兼容映射
```

同时新增 `QUALITY_BAND`，避免继续把 holistic quality 与 release decision 混为一谈。

---

## 6. 第三阶段：隔离并修复测试语料

## 6.1 先 quarantine 受污染案例

将以下案例标记：

```yaml
adjudication:
  status: quarantine
  reason: fixture-invalid-or-contract-ambiguous
```

案例：

```text
GN-EXP-001
GN-ROADMAP-001
BP-002-fail
BP-005-pass
GN-PROP-001
```

quarantine 案例不得进入准入指标。

## 6.2 修复 `GN-EXP-001`

### 当前问题

文档仍保留：

- 训练命令；
- TensorFlow models 仓库；
- 数据处理；
- 完整超参数；
- learning-rate schedule；
- 输出说明；
- 性能评估方式。

因此它不是纯粹的“load-bearing claim 无 handle”。

### 推荐拆分为两个案例

#### `GN-EXP-REPRO-001`

目标：测试实验可复现性。

删除或模糊：

- code commit；
- framework version；
- environment；
- hardware；
- random seed；
- exact command；
- hyperparameters；
- dataset version；
- expected tolerance。

仍保留结果数字。

预期不再强制使用 HF-12A，而是：

```yaml
required_findings:
  - missing-code-version
  - missing-environment
  - missing-execution-entry
  - missing-reproduction-tolerance
```

是否需要新增专属 hard gate，应在 ADR 中决定。

#### `GN-EVIDENCE-BARE-CLAIM-001`

目标：纯测 HF-12A。

文档仅保留：

```markdown
# Result

The model achieves 74.0% top-1 accuracy.
```

不得包含：

- source；
- experiment ID；
- commit；
- config；
- chart；
- path；
- assumption/HYPOTHESIS 标记。

预期：

```yaml
required_blockers: [HF-12A]
```

## 6.3 修复 `GN-ROADMAP-001`

真正删除 Phase 1 中：

```text
GO
MODIFY
STOP
numeric threshold
downstream route
```

只保留：

```markdown
- 验收：与基线对照，效果达标即可，具体算例与阈值届时定。
```

必须增加 mutation 后置断言：

```yaml
assert_absent:
  - "- **GO:**"
  - "- **MODIFY:**"
  - "- **STOP:**"
  - "20% error reduction"
  - "proceed to Phase 2"

assert_present:
  - "届时定"
```

同时保留：

- committed phase 标记；
- research question；
- minimal experiment；
- 文档其他阶段不变。

预期：

```yaml
required_blockers: [HF-15]
forbidden_blockers: [HF-13, HF-14a, HF-14b]
```

## 6.4 修复 `BP-002-fail`

目标仅测试 HF-14b。

删除：

```text
status: DECIDED
The core is done.
design review in progress
```

或改为无矛盾版本：

```yaml
document_lifecycle: ACCEPTED
```

正文：

```markdown
当前 69 项测试全部通过。
```

不得提供：

- 时间戳；
- status canonical source；
- “snapshot as of”；
- 可更新指针。

预期：

```yaml
required_blockers: [HF-14b]
forbidden_blockers: [HF-13, HF-14a, HF-15]
```

## 6.5 修复 `BP-005-pass`

改为：

```yaml
document_lifecycle: ACCEPTED
```

正文保持：

```text
HYPOTHESIS
尚未验证
project-inference
to-verify experiment
```

不得使用 `status: DECIDED`。

预期：

```yaml
quality_band: PASS
gate_decision: ALLOW
forbidden_blockers: [HF-3, HF-10, HF-12E, HF-14a]
```

## 6.6 修复 `GN-PROP-001`

删除目标章节时，同时清理：

- TOC 条目；
- signoff checklist；
- 本文其他指向已删除章节的链接；
- “这些章节已存在”一类声明。

增加：

```yaml
assert_no_dangling_toc: true
assert_no_signoff_contradiction: true
```

其目的应仅为：

```text
proposal lacks required test/graduation/rollback content
```

不得用 HF-14a 评价导航残留。

---

## 7. 第四阶段：升级 mutation 生成与语料验证

## 7.1 mutation 不得只验证“脚本运行成功”

每个 mutation 结果必须具有：

```yaml
postconditions:
  target_defect_present: true
  intended_positive_anchor_absent: true
  unrelated_sections_unchanged: true
  no_dangling_toc_entries: true
  no_secondary_state_conflict: true
  no_unexpected_status_change: true
```

## 7.2 增加语义后置检查

新增脚本建议：

```text
scripts/validate_mutation_semantics.py
```

至少支持：

- 指定字符串必须消失；
- 指定字符串必须出现；
- TOC anchor 必须解析；
- 删除章节后不得保留 signoff claim；
- 单缺陷 mutation 不得引入新的状态矛盾；
- boundary pair 只允许声明的字段或正文范围不同；
- 同字节不同 profile 对必须验证文档 SHA-256 相同。

## 7.3 mutation 输出变更摘要

每次生成必须输出：

```yaml
mutation_result:
  case_id:
  mutation_id:
  base_sha256:
  mutated_sha256:
  changed_ranges:
  required_absent_checks:
  required_present_checks:
  unchanged_region_hashes:
  semantic_validation:
    status: PASS | FAIL
    findings: []
```

语义验证失败的 case 自动进入 quarantine。

---

## 8. 第五阶段：只实施确定的 Skill 修改

## 8.1 F1：profile-aware HF-9

修改位置：

```text
.claude/skills/documentation-quality-evaluator/SKILL.md
evals/skills/harness/hard-fail.md
evals/skills/harness/checkers/frontmatter_check.py
evals/skills/harness/make_grading_injection.py
scripts/make_eval_plan.py
```

要求：

- `evaluation_profile.provenance_policy` 必须成为显式输入；
- evaluator 报告必须回显 profile；
- checker 不应脱离 profile 独立给出最终 blocker；
- `frontmatter_check.py` 可以输出 raw finding，但最终严重度由 profile policy 决定。

建议 checker 输出：

```json
{
  "check": "traceability-frontmatter",
  "finding": "missing",
  "profile_required": true,
  "raw_status": "FOUND",
  "final_gate": "UNDECIDED"
}
```

由 evaluator 根据 profile 转换为：

```text
controlled → HF-9 BLOCKER
legacy → MAJOR migration finding
external → MINOR/N/A
```

## 8.2 F2：收紧 HF-13

HF-13 只有在以下条件全部成立时触发：

1. 至少两个正式 artifact role；
2. 两个 role 有不同 canonical source；
3. 两个 role 有不同自然更新频率；
4. 角色均为 body-level primary content；
5. 没有清楚的 appendix/link subordination；
6. 已造成 observable harm：
   - duplication；
   - drift；
   - contradiction；
   - ownership 不清；
   - reader 无法确认 canonical document。

明确不触发：

- architecture doc 中有一段 maturity snapshot；
- roadmap 中有 10–20 行 architecture summary；
- ADR 中记录少量 implementation consequences；
- 一个 accepted doc 含 open questions；
- 单纯章节多；
- 单纯篇幅长。

输出必须列出：

```text
role A
role B
canonical source A/B
update frequency A/B
observable harm
```

缺一项不得触发 HF-13。

## 8.3 F3：收紧 HF-14a

HF-14a 只适用于：

> 同一作用域、同一时间语义、同一状态变量的两个不兼容断言。

例如：

```text
59 tests pass
69 tests pass
```

且两者都声称当前状态。

明确不属于 HF-14a：

- TOC 悬空；
- 章节被删除；
- metadata 字段缺失；
- document lifecycle 与 claim status 不同；
- stable architecture 仍有 non-blocking open question；
- `DECIDED` architecture 中仍有未来优化问题；
- 一处是历史快照，另一处是当前值且日期明确。

对于悬空 TOC，应归入：

```text
link/navigation integrity
```

而非状态矛盾。

## 8.4 暂不修改 HF-12A 和 HF-15

在修复后的测试重新运行前：

```text
HF-12A: no logic change
HF-15: no logic change
```

只有满足以下条件才立项：

```text
corrected fixture validated
gold re-adjudicated
3 independent runs
same target blocker missed ≥2 times
no secondary defect
```

---

## 9. 第六阶段：重新审定 gold

## 9.1 reviewer 不得读取

Reviewer A/B 不得读取：

```text
DQE SKILL.md
hard-fail.md
rubric.md
evaluator output
manifest expected fields
case_id 所暗示的类别
```

## 9.2 reviewer 需要分别给出两轴判断

```text
QUALITY_BAND=PASS|PARTIAL|FAIL
GATE_RECOMMENDATION=ALLOW|BLOCK|INCOMPLETE
DEFECT_TAGS=[...]
CONFIDENCE=...
```

## 9.3 gold 锁定要求

每个修复后的 case 需要：

- Reviewer A；
- Reviewer B；
- mutation semantic validator；
- manifest validator；
- 用户或独立 adjudicator 处理分歧；
- 不得用 DQE 自身输出决定 expected verdict。

## 9.4 原 gold 不自动继承

修复后的 case 必须增加 `case_version`，例如：

```yaml
case_version: 2
```

不得直接沿用 v1 的 adjudication。

---

## 10. 第七阶段：先运行小型诊断矩阵

不要立即重跑完整 26 次。

### 10.1 诊断矩阵

建议：

| 组 | 案例 | 重复数 | 目的 |
|---|---|---:|---|
| Profile | BP-004-external | 3 | external HF-9 豁免 |
| Profile | BP-004-controlled | 3 | controlled HF-9 blocker |
| Status schema | BP-005-pass-v2 | 3 | hypothesis 不误触发 |
| Evidence | BP-005-fail | 3 | bare VERIFIED 应阻断 |
| Volatile state | BP-002-pass | 3 | dated pointer 逃逸 |
| Volatile state | BP-002-fail-v2 | 3 | 仅触发 HF-14b |
| Roadmap | GN-ROADMAP-001-v2 | 3 | 纯 HF-15 召回 |
| Experiment | GN-EXP-REPRO-001 | 3 | 可复现性判定 |
| Claim | GN-EVIDENCE-BARE-CLAIM-001 | 3 | 纯 HF-12A |
| Proposal | GN-PROP-001-v2 | 3 | 不误触发 HF-14a |

总计建议 30 runs。

### 10.2 诊断矩阵通过条件

```text
profile pair ordering = 100%
每个 case verdict/gate decision 3/3 一致
每个 required blocker 召回 = 100%
forbidden blocker violation = 0
HF-13 不在单 role doc 上触发
HF-14a 不因 TOC/metadata 触发
```

### 10.3 诊断结果的决策规则

#### corrected HF-12A case 仍漏判

才修改 HF-12A。

#### corrected HF-15 case 仍漏判

才修改 HF-15。

#### corrected cases 通过

保持 HF-12A/HF-15 不变，避免过度调严。

---

## 11. 第八阶段：补 baseline-no-skill

当前测试只能衡量：

> DQE 是否符合自己定义的规则。

还需要衡量：

> DQE 是否比裸模型更可靠。

每个诊断 case 增加：

```text
without_skill
with_dqe_v0.3
with_dqe_v0.4
```

建议比较：

- gate decision accuracy；
- required finding recall；
- forbidden blocker rate；
- verdict stability；
- 是否错误依赖上下文；
- 输出成本；
- 报告可执行性。

DQE 至少应在以下方面优于裸模型：

```text
严重问题召回
profile 一致性
状态矛盾精度
不预测虚假 PASS
稳定性
结构化输出
```

---

## 12. 第九阶段：完整准入矩阵

诊断矩阵通过后，重建完整 blind suite。

### 12.1 扩大稳定性样本

不再只测 3 个 case。

至少：

```text
5 个案例 × 3 次
```

应覆盖：

- positive external；
- positive controlled；
- negative roadmap；
- negative experiment/evidence；
- mixed-role negative。

### 12.2 完整指标

至少统计：

```text
golden-negative false allow
golden-positive false block
required blocker recall
forbidden blocker violation
boundary-pair ordering
verdict/gate consistency
blocker-set Jaccard
score standard deviation
profile compliance
baseline gain
```

### 12.3 不计入指标的案例

以下状态不得计入准入指标：

```text
candidate
quarantine
disputed
contract-pending
semantic-validation-failed
```

---

## 13. Batch 2 解锁标准

DQE 只有同时满足以下条件，才可从：

```text
experimental
```

提升为：

```text
provisional-gate
```

### 13.1 数据质量条件

```text
0 invalid fixture
0 unresolved gold dispute
所有 mutation semantic validation 通过
所有 boundary pair 的 declared difference 可验证
```

### 13.2 判别条件

```text
golden-negative GATE_DECISION false ALLOW = 0
golden-positive false BLOCK = 0
required blocker recall ≥ 0.90
forbidden blocker violation = 0
boundary-pair ordering = 100%
```

### 13.3 稳定性条件

```text
至少 5 cases × 3 runs
gate decision 一致率 = 100%
核心 blocker 集合高度一致
最大 score σ ≤ 5
```

### 13.4 能力增益条件

```text
DQE 在严重问题召回或稳定性上明确优于 baseline-no-skill
不存在只增加篇幅而不增加判别质量的情况
```

### 13.5 运行姿态

即使提升为 `provisional-gate`，仍应保持：

```yaml
disable-model-invocation: true
auto_trigger: false
invocation: manual-orchestrator-only
```

直到积累更多真实项目文档。

---

## 14. Agent 执行顺序

Agent 应严格按以下顺序工作：

### Step 1：审计与冻结

- 记录当前 commit；
- 创建 baseline tag；
- 建立 defect ledger；
- 不修改旧结果。

### Step 2：创建 ADR

- 定义 evaluation profile；
- 定义双轴 verdict；
- 定义 document lifecycle；
- 定义 experiment reproducibility policy。

### Step 3：quarantine

- 标记 5 个污染案例；
- 从准入聚合中排除；
- 更新 benchmark changelog。

### Step 4：修 fixtures 和 mutation generator

- 修正案例；
- 增加 postconditions；
- 新增 semantic validator；
- case version +1。

### Step 5：重新双评审

- A/B 隔离审定；
- 记录 quality 与 gate 两轴；
- 分歧不得自动消解。

### Step 6：最小 Skill 修改

仅修改：

```text
HF-9 profile
HF-13
HF-14a
profile input plumbing
```

暂不修改：

```text
HF-12A
HF-15
```

### Step 7：诊断矩阵

- 运行 30 次左右；
- 输出逐案归因；
- 决定是否需要修 HF-12A/HF-15。

### Step 8：必要的二次 Skill 修改

仅对 corrected fixture 稳定暴露的问题修改。

### Step 9：完整矩阵与 baseline

- 重建 blind suite；
- 运行 current + repeat；
- 运行 without-skill baseline；
- 聚合双轴指标。

### Step 10：准入决定

输出：

```text
PROMOTION=YES|NO
NEW_STATUS=experimental|provisional-gate
BATCH_2_UNLOCKED=true|false
```

---

## 15. 要求生成的产物

### 契约

```text
docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md
docs/skill-development/reports/dqe-v0.4-defect-ledger.md
```

### Skill

```text
.claude/skills/documentation-quality-evaluator/SKILL.md
evals/skills/harness/hard-fail.md
evals/skills/harness/rubric.md
```

### Harness

```text
evals/skills/harness/checkers/frontmatter_check.py
evals/skills/harness/checkers/status_vocab_check.py
evals/skills/harness/make_grading_injection.py
evals/skills/harness/score_grading.py
scripts/make_eval_plan.py
scripts/validate_mutation_semantics.py
```

### Corpus

```text
GN-EXP-REPRO-001
GN-EVIDENCE-BARE-CLAIM-001
GN-ROADMAP-001 v2
BP-002-fail v2
BP-005-pass v2
GN-PROP-001 v2
```

### Reports

```text
docs/testing/corpus-repair-report-v4.md
docs/testing/adjudication-v4.md
docs/skill-development/reports/dqe-v0.4-diagnostic-matrix.md
docs/skill-development/reports/dqe-v0.4-full-admission-report.md
```

---

## 16. 变更控制要求

每次修改必须说明：

```yaml
change_id:
reason:
evidence:
files_changed:
cases_expected_to_change:
cases_expected_not_to_change:
risk:
rollback:
```

不得进行以下操作：

- 根据一个失败案例修改多个无关 hard gate；
- 为了让指标变绿而改 gold label；
- 把真实 secondary defect 从报告中删除但不修 fixture；
- 覆盖 v0.3 结果；
- 使用待测 DQE 参与 gold 初次审定；
- 未通过诊断矩阵就运行完整准入并宣称完成。

---

## 17. 给 Agent 的启动提示词

```text
你正在升级 research-code-docs 仓库中的 documentation-quality-evaluator。

目标不是让当前指标变绿，而是建立有效、可归因、可重复的文档质量准入测试。

严格按以下顺序执行：

1. 读取：
   - docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md
   - 本计划
   - .claude/skills/documentation-quality-evaluator/SKILL.md
   - evals/skills/harness/hard-fail.md
   - evals/skills/harness/rubric.md
   - 相关 manifests、fixtures、mutation scripts、blind-run outputs

2. 创建 defect ledger。将每个问题分类为：
   - SKILL
   - FIXTURE
   - CONTRACT
   - HARNESS
   不得继续使用“各占一半”这种无法执行的粗略归因。

3. 先创建 ADR，决定：
   - evaluation_profile
   - provenance_policy
   - QUALITY_BAND 与 GATE_DECISION
   - document_lifecycle 与 claim status 的边界
   - experiment reproducibility 的评价归属

4. 将 GN-EXP-001、GN-ROADMAP-001、BP-002-fail、
   BP-005-pass、GN-PROP-001 暂时 quarantine。
   Quarantine 案例不得进入准入指标。

5. 修复 mutation：
   - GN-ROADMAP 必须真正删除所有 GO/MODIFY/STOP 和数值门；
   - GN-EXP 拆成复现性案例和裸 claim HF-12A 案例；
   - BP-002 删除附带状态矛盾；
   - BP-005 使用 document_lifecycle，不再使用 status: DECIDED；
   - GN-PROP 清理 TOC/signoff 残留。
   给 mutation 增加语义后置断言。

6. 重新用隔离 Reviewer A/B 审定。Reviewer 不得读取 DQE、hard-fail、
   rubric、manifest expected 或 evaluator outputs。
   Reviewer 同时输出 QUALITY_BAND 与 GATE_RECOMMENDATION。

7. 仅修改确定的 Skill 问题：
   - profile-aware HF-9
   - 收紧 HF-13
   - 收紧 HF-14a
   不得先修改 HF-12A 或 HF-15。

8. 运行小型诊断矩阵，每个关键案例运行 3 次。
   corrected HF-12A/HF-15 case 若仍稳定漏判，才立项修改对应 Skill。

9. 诊断通过后，再运行完整 blind matrix 和 baseline-no-skill。

10. 最终报告必须明确：
    - 哪些变化修复了测试；
    - 哪些变化修复了 Skill；
    - 哪些原失败被判定为无效测试；
    - 是否满足 provisional-gate；
    - 是否解锁 Batch 2。

禁止：
- 为了通过测试而放宽或强化无关 hard gate；
- 使用 DQE 自己生成 gold；
- 覆盖历史结果；
- 在 quarantine 未清零前宣称准入通过；
- 将文档整体质量与 gate 放行决定继续混为一个未经解释的标签。
```

---

## 18. 最终决策规则

本轮的核心原则是：

> 测试必须先证明自己测到了目标缺陷，才有资格要求 Skill 因此改变。

因此：

```text
测试缺陷未修复
→ 不修改对应 Skill

fixture 已修复且通过语义验证
→ 重新盲测

corrected fixture 稳定漏判
→ 修改 Skill

corrected fixture 稳定判对
→ 保持 Skill，不做过度强化
```

本计划完成后，才可对 DQE 是否达到 `provisional-gate` 做有效判断。当前 v0.3 不应被废弃，但也不能作为后续文档的正式自动准入门。
