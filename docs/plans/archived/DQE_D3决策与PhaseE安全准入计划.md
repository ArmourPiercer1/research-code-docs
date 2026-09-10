# DQE v0.4 D.3 复核决策与 Phase E 安全准入计划

> 仓库：`ArmourPiercer1/research-code-docs`  
> 当前候选：`documentation-quality-evaluator` v0.4.0（D-16 修正后）  
> 日期：2026-08-05  
> 状态：**Phase E 条件批准；完成运行安全前置项后执行**

---

## 0. 最终决策

```text
D16_DECISION=ACCEPT
CANDIDATE_VERSION=0.4.1
PHASE_D=PASS_8_OF_8
OQ_REPRO=RESOLVED_OPTION_A
HF_REPRO=NOT_ADOPTED
PHASE_E=APPROVED_WITH_PRECONDITIONS
BACKGROUND_WORKFLOW_FOR_ADMISSION=FORBIDDEN
```

### 决策解释

1. **接受 D-16 的三规则 gate 推导。**

   ```text
   缺少必需输入/章节/执行步骤 → INCOMPLETE
   存在经 profile 映射后的 blocker → BLOCK
   其余 → ALLOW
   ```

   `QUALITY_BAND` 继续承载 rubric 总分与整体质量；`FACTUAL_VALIDITY=UNVERIFIED` 不改变
   `GATE_DECISION`，但会阻止“绿色终端门”。

2. **D-16 是可观察行为变化，不应继续与修正前版本共用同一个版本号。**

   将候选版本从 `0.4.0` 提升为：

   ```text
   0.4.1
   ```

   冻结修正前的 v0.4.0，以便复现首次 D.3 的三态不稳定。

3. **确认 OQ-REPRO=A。**

   - `BP-006-audit`：`external + audit → PARTIAL / ALLOW`
   - `BP-006-release`：`controlled + release-gate → BLOCK`
   - 不新增 `HF-REPRO`

4. **Phase D 视为完成。**

   D.3 修复后：

   - `BP-006-release`：BLOCK ×3；
   - `BP-006-audit`：ALLOW ×3；
   - `GP-EXP-001`：ALLOW，checker 实际读取 1 个文件；
   - diagnostic 达到 8/8。

5. **批准 Phase E，但只有完成本文前置安全项后才允许启动。**

---

# 1. 对 63M-token 失控事件的定性

## 1.1 归类

该事件不是：

- DQE Skill 质量失败；
- corpus 污染；
- evaluator 输出错误；
- promotion 结果。

应记录为：

```text
INCIDENT_CLASS=HARNESS_ORCHESTRATION_FAILURE
SEVERITY=HIGH_COST_NO_DATA_CORRUPTION
```

根因是参数类型从 array 变成 JSON string 后，脚本逐字符迭代，并为每个字符生成 agent。

## 1.2 数据状态

根据当前记录：

- evaluator 是只读的；
- aggregation 未运行；
- corpus、Skill 和正式 results 未被写入。

因此：

```text
CORPUS_CLEANUP=NOT_REQUIRED
RESULT_CLEANUP=NOT_REQUIRED
```

但必须完成治理修复：

- 事故写入 benchmark changelog；
- 无效 run 不计入任何指标；
- 保存 run ID、失败原因、消耗和“无输出”证明；
- 增加静态 run-plan 和 hard cap；
- 禁止 Phase E 使用同类 background Workflow。

---

# 2. Phase E 前必须完成的仓库一致性修正

## 2.1 候选版本改为 0.4.1

需要同步：

```text
.claude/skills/documentation-quality-evaluator/SKILL.md
docs/skill-development/skills-registry.yaml（或实际 registry）
docs/skill-development/reports/dqe-v0.4-skill-change-summary.md
docs/skill-development/reports/dqe-v0.4-diagnostic-matrix.md
docs/testing/benchmark-changelog.md
```

记录：

```yaml
skill_version: 0.4.1
change:
  id: D-16
  type: gate-composition-contract-fix
  thresholds_changed: false
  observable_behavior_changed: true
```

同时更新 `last_verified`。

## 2.2 冻结三个可复现 bundle

不得手工“把 v0.4 改回 v0.3”。

创建：

```text
evals/skills/snapshots/dqe-v0.3.0/
evals/skills/snapshots/dqe-v0.4.0-pre-d16/
evals/skills/snapshots/dqe-v0.4.1-candidate/
```

每个 bundle 至少包含：

```text
SKILL.md
hard-fail.md
rubric.md
canonical-source-map.md
EVALUATOR_CONTRACT
checker/version manifest
SNAPSHOT-MANIFEST.yaml
```

`SNAPSHOT-MANIFEST.yaml`：

```yaml
version:
source_commit:
created_at:
files:
  - path:
    sha256:
```

v0.3 必须从历史 Git commit 提取，不得依赖记忆重建。

## 2.3 更新 canonical diagnostic report

当前 canonical diagnostic 文档仍可能保留“7/8、Phase E held”的旧状态。应在 Phase E 前：

- 更新为 8/8；或
- 保持原报告不可变，并新增正式 D.3 addendum。

推荐新增：

```text
docs/skill-development/reports/dqe-v0.4.1-diagnostic-close.md
```

内容至少包括：

- runaway incident；
- 七次 direct rerun；
- D-16 根因；
- D-16 修改前后结果；
- BP-006 pair；
- stale-path 修复；
- 8/8 结论；
- candidate commit SHA。

---

# 3. 终端门语义的最后澄清

D-16 后，`GATE_DECISION=ALLOW` 不必然等于下游可以继续。

应显式派生：

```text
TERMINAL_GREEN =
  GATE_DECISION == ALLOW
  AND FACTUAL_VALIDITY != UNVERIFIED
  AND CHECKER_STATUS == COMPLETE
  AND READER_TEST == PASS
```

因此：

```text
external + audit
PARTIAL + ALLOW + UNVERIFIED
```

表示：

> 文档审计没有发现 profile 下的 blocker，但它不是绿色终端门。

## 3.1 不要求再次修改 Skill schema

为避免 Phase E 前继续扩大 Skill 改动，暂不要求增加新的输出字段。

由 aggregator 派生：

```text
terminal_green: true | false
```

## 3.2 manifest 增加可选预期

```yaml
expected:
  gate_decision: ALLOW
  terminal_green: false
```

适用于：

- external audit；
- source 未核验；
- reader test 失败但 audit 仍 ALLOW。

受控、正式 release positive 可要求：

```yaml
terminal_green: true
```

## 3.3 新增准入指标

```text
terminal_contract_mismatch_count == 0
```

没有这一指标，DQE 可能在 gate 轴正确，但仍无法证明它能安全充当 terminal quality gate。

---

# 4. Phase E 运行器的强制安全设计

## 4.1 禁止动态 workflow

Phase E 不得使用：

- background Workflow；
- 接收任意 JSON 后自行迭代的通用脚本；
- agent 输出驱动的新 agent 创建；
- 无上限递归或嵌套 fan-out。

只允许：

```text
静态 plan
→ schema validation
→ 有界 direct Agent calls
→ 每批 checkpoint
→ 最终 aggregation
```

## 4.2 静态计划格式

先生成：

```text
tests/corpus/blind-runs/<run-id>/phase-e-plan.json
```

每个条目：

```json
{
  "run_key": "v041__BP-006-audit__1",
  "arm": "v0.4.1",
  "case_id": "BP-006-audit",
  "run_idx": 1,
  "snapshot": "dqe-v0.4.1-candidate",
  "input_path": "...",
  "profile_path": "...",
  "max_turns": 24
}
```

## 4.3 plan validator

新建或增强：

```text
scripts/validate_eval_plan.py
```

必须检查：

```text
args 是 JSON array，而不是 string
每个元素是 object
run_key 全局唯一
case_id 存在且为 live gold
snapshot 存在且 hash 验证通过
run_idx 在允许范围
计划总数 <= MAX_EVAL_RUNS
每个 case/arm 的次数不超过上限
没有 quarantine/disputed/candidate
没有未知 arm
```

任何错误：

```text
ABORT_BEFORE_AGENT_CALL
```

## 4.4 运行硬限制

建议：

```yaml
MAX_EVAL_RUNS: 64
MAX_CONCURRENCY: 2
MAX_BATCH_SIZE: 4
MAX_EVALUATOR_AGENTS_PER_RUN: 1
MAX_READER_AGENTS_PER_RUN: 1
MAX_NESTING_DEPTH: 1
MAX_TURNS_PER_EVALUATOR: 24
MAX_RETRIES_PER_SLOT: 1
```

若计划超过 64 次，必须重新裁剪，不能自动放宽。

## 4.5 批次执行

每 4 次为一批：

```text
运行 4 个
→ 检查 agent 数、token、结果 schema、文件读取
→ 写 checkpoint
→ 再进入下一批
```

异常时只重跑失败 slot，不重跑整个 arm。

## 4.6 token 预算

此前 39 次 diagnostic 约使用 3.6M tokens，平均约：

```text
~92k tokens / evaluator slot
```

Phase E 建议总 slot 控制在 60 左右：

```text
expected ≈ 5.5M tokens
hard planning ceiling = 7.0M tokens
```

达到预算的 80% 时停止创建新 slot，先聚合已有结果并人工复核。

---

# 5. Phase E 矩阵设计

不建议三个 arm 都对全部 live corpus 做完整重复。

把“候选准入”和“比较价值”拆开。

## 5.1 Arm A：v0.4.1 正式准入

运行：

```text
全部 live gold cases ×1
+
5 个稳定性案例额外 ×2
```

即每个稳定性案例共 3 次。

建议稳定性案例：

```text
BP-004-external
BP-006-audit
BP-006-release
GN-ROADMAP-001
GP-PROP-CONTROLLED-001
```

覆盖：

- profile-aware HF-9；
- D-16 audit ALLOW；
- controlled reproducibility BLOCK；
- HF-15；
- 正常 controlled positive。

若 live case 数为 `N`：

```text
Arm A slots = N + 10
```

## 5.2 Arm B：冻结 v0.3 对照

无需对所有 live case 运行。

使用固定的 13-case diagnostic subset，一次即可：

```text
Arm B slots = 13
```

重点证明 v0.4.1 相对 v0.3 修复了：

- external HF-9 false BLOCK；
- audit HF-14b false BLOCK；
- profile echo 缺失；
- 双轴 verdict；
- D-16 audit gate composition。

## 5.3 Arm C：no-skill baseline

对同一 13-case subset 运行一次：

```text
Arm C slots = 13
```

baseline prompt 只提供：

- target；
- evaluation profile；
- 两轴输出字段含义；
- 中性 finding-code 输出格式。

不得提供：

- DQE hard-fail；
- DQE rubric；
- expected labels；
- case class。

## 5.4 预计规模

```text
total slots = N + 36
```

若 preflight 验证得到 `N=25`：

```text
total = 61
```

该数字必须由脚本打印并经人工确认，本文不把 25 当作硬编码事实。

---

# 6. Phase E 自动评分要求

## 6.1 Candidate arm 的硬准入指标

```text
gate_expectation_mismatch_count == 0
terminal_contract_mismatch_count == 0
golden_negative_false_allow == 0
golden_positive_false_non_allow == 0
required_blocker_recall >= 0.90
required_finding_recall >= 0.90
forbidden_blocker_violation_rate == 0
boundary_pair_ordering == 1.0
three_run_gate_consistency == 1.0
profile_echo_compliance == 1.0
checker_execution_compliance == 1.0
max_score_stddev <= 5
```

`checker_execution_compliance` 要求每次：

```text
CHECKER_STATUS=COMPLETE
files_checked >= 1
checker target 与 manifest document 一致
```

## 6.2 finding-code 不能缺失

一个 case 即使 gate 正确，但没有达到 required-finding recall，也不能通过。

防止：

> 因错误理由得到正确 BLOCK。

## 6.3 baseline 比较指标

比较 arm 不直接决定 candidate pass/fail，但 v0.4.1 必须证明有增益。

最低要求：

1. 在全部已知 profile-sensitive cases 上，不得劣于 v0.3；
2. v0.4.1 的 gate mismatch 数严格少于 v0.3；
3. v0.4.1 的 required-finding recall 不低于 no-skill；
4. v0.4.1 在以下至少两项优于 no-skill：
   - gate accuracy；
   - finding recall；
   - forbidden blocker rate；
   - repeated-run consistency；
   - schema/profile compliance。

---

# 7. Phase E 的执行许可

给本地 Agent 的回复应为：

```text
可以进入 Phase E，但不是立即启动无界 3-arm Workflow。

先完成：
1. 候选版本 0.4.1 与三个 snapshot；
2. canonical diagnostic 8/8 更新；
3. static phase-e-plan.json；
4. validate_eval_plan.py；
5. MAX_EVAL_RUNS=64 等硬限制；
6. terminal_contract 指标；
7. 2-slot canary。

然后：
- 先展示 exact N、三个 arm 的 slot 数、总 slot 数和预算；
- canary 通过后，按 4-slot direct batches 执行；
- 不使用 background Workflow；
- 不允许脚本根据字符串或 agent 输出动态扩张。
```

---

# 8. 两次 canary

正式矩阵前只运行：

```text
v0.4.1 / BP-006-audit / run 1
v0.4.1 / BP-006-release / run 1
```

检查：

```text
audit = PARTIAL / ALLOW / terminal_green=false
release = BLOCK / HF-9 silent
finding codes 完整
files_checked >= 1
无额外 agent fan-out
```

canary 不通过则 Phase E 自动停止。

---

# 9. Promotion 与 Batch 2

## 9.1 通过时

```yaml
documentation-quality-evaluator:
  version: 0.4.1
  status: provisional-gate
  disable-model-invocation: true
  auto_trigger: false
  invocation: manual-orchestrator-only
  terminal_gate_authority: limited
```

继续保持：

- 不安装到日常 Claude Code 环境；
- 不自动触发；
- 不自动发布；
- 不自动修改被评估文档；
- 关键 ALLOW 保留人工抽查。

随后解锁 Batch 2。

## 9.2 Batch 2 顺序

建议：

```text
1. document-information-architect
2. workspace-forensics-and-inventory
3. research-question-and-literature-planner
4. research-evidence-synthesizer
```

优先 IA 和 workspace forensics，因为它们能持续产生真实 corpus，降低后续对 synthetic fixtures 的依赖。

## 9.3 未通过时

不得进行 broad rewrite。

按失败类别处理：

```text
HARNESS → 修 runner，只重跑受影响 slots
FIXTURE → quarantine / re-adjudicate
CONTRACT → ADR 小修 + 定向诊断
SKILL → 只有干净 fixture 3 次中至少 2 次稳定复现才修改
```

---

# 10. 给本地 Agent 的执行提示词

```text
Phase E 获得条件批准。

先不要启动任何 background Workflow。

决策：
- 接受 D-16 三规则 gate derivation；
- 候选版本改为 0.4.1；
- OQ-REPRO=A，禁止新增 HF-REPRO；
- Phase D 已通过 8/8；
- 63M-token 事件归为 HARNESS_ORCHESTRATION_FAILURE，无 corpus 清理，但必须加运行硬边界。

前置任务：
1. 冻结 dqe-v0.3.0、dqe-v0.4.0-pre-d16、dqe-v0.4.1-candidate 三个完整 bundle，
   每个文件记录 SHA-256 和 source commit。
2. 更新 canonical diagnostic，明确 D.3=8/8 和 D-16。
3. 新增 validate_eval_plan.py，拒绝 string args、重复 run_key、未知 case、超出 MAX_EVAL_RUNS。
4. 设置：
   MAX_EVAL_RUNS=64
   MAX_CONCURRENCY=2
   MAX_BATCH_SIZE=4
   MAX_NESTING_DEPTH=1
   MAX_RETRIES_PER_SLOT=1
5. aggregator 增加 terminal_green 和 terminal_contract_mismatch_count。
6. 所有 run 要求 checker files_checked>=1。
7. 生成静态 phase-e-plan.json，不允许由 agent 输出动态增加任务。

矩阵：
- Arm A v0.4.1：全部 live gold ×1，指定 5 cases 额外 ×2。
- Arm B frozen v0.3：13-case diagnostic subset ×1。
- Arm C no-skill：同一 13-case subset ×1。
- 总 slots=N+36；先打印 exact N、各 arm 数量、总数和预算。
- 运行两次 canary：BP-006-audit、BP-006-release。
- canary 通过后，以 4-slot direct batches 执行。
- 禁止 background workflow 和无界 loop。

最终输出：
- exact plan 与 hash；
- 每批 token/agent 计数；
- candidate admission metrics；
- v0.3/no-skill 对照；
- promotion decision；
- Batch 2 unlock decision。
```

---

## 11. 核心原则

> 这次失控不是缩减测试严谨性的理由，而是把“科学评测计划”与“任务调度器”分离的理由。

Phase E 可以继续，但其任务集合必须在第一个 agent 启动前完全确定、校验、计数并封顶。
