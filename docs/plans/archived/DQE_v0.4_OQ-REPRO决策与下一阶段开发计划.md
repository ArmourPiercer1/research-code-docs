# DQE v0.4 OQ-REPRO 决策与下一阶段开发计划

> 适用仓库：`ArmourPiercer1/research-code-docs`  
> 当前 Skill：`documentation-quality-evaluator` v0.4.0  
> 当前语料：dataset version 4  
> 主要依据：
>
> - `docs/skill-development/reports/dqe-v0.4-oq-repro-decision.md`
> - `docs/skill-development/reports/dqe-v0.4-skill-change-summary.md`
> - `docs/skill-development/reports/dqe-v0.4-diagnostic-matrix.md`
> - `docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md`
> - `tests/corpus/cases/golden-negative/GN-EXP-REPRO-001/manifest.yaml`
>
> 决策状态：本文给出 OQ-REPRO 最终决策，并规定 Phase E 前的语料、harness 和轻量一致性修复。  
> 日期：2026-08-02

---

## 0. 最终决策

选择报告中的 **Option A：拆分为 profile pair**。

```text
OQ_REPRO_DECISION=A
HF_REPRO=REJECTED_FOR_V0_4
```

具体含义：

1. 当前 `GN-EXP-REPRO-001` 的正文缺陷是真实的，但它的 profile 是：

   ```yaml
   provenance_policy: external
   decision_mode: audit
   ```

   在该 profile 下，正确结果应为：

   ```text
   QUALITY_BAND=PARTIAL
   GATE_DECISION=ALLOW
   ```

   即：明确报告不可复现问题，但不把外部上游文档的 advisory audit 解释为本地发布阻断。

2. 新增一个受控发布门案例，使用相同的不可复现正文，但补齐本地 traceability frontmatter，并采用：

   ```yaml
   provenance_policy: controlled
   decision_mode: release-gate
   ```

   预期：

   ```text
   GATE_DECISION=BLOCK
   ```

   且必须证明 BLOCK 独立于 HF-9，由现有 rubric、reader test、HF-12A/E 或 non-compensatory rule 产生。

3. **不新增 `HF-REPRO`。**

   现有证据已经证明：

   - `external + audit` 下 `PARTIAL/ALLOW` 是 profile 契约的预期行为；
   - `controlled + release-gate` 下现有规则已经连续两次得到 `FAIL/BLOCK`；
   - 新增 hard gate 不会改变 audit 案例结果，反而扩大 Skill 改动并提高过度阻断风险。

4. 本轮问题归类为：

   ```text
   CORPUS_SPEC_MISMATCH
   ```

   而不是新的 DQE 判别缺陷。

---

# 1. 决策依据

## 1.1 v0.4 的 profile 行为是正确的

诊断矩阵中，`GN-EXP-REPRO-001` 在 `external + audit` 下连续三次得到：

```text
QUALITY_BAND=PARTIAL
GATE_DECISION=ALLOW
BLOCKERS=[]
```

评估器没有忽略缺陷，而是稳定识别了：

- 缺少训练命令；
- 缺少超参数和学习率计划；
- 缺少随机种子；
- 缺少代码与框架版本；
- 缺少硬件信息；
- 数据和结果依赖作者控制的 HDFS；
- 部分图表与 notebook 链接不可用。

这些问题被写成 MAJOR findings，因此整体质量是 `PARTIAL`。没有 BLOCK，是因为调用模式是针对外部文档的 advisory audit。

这正是 v0.4 为修复 HF-9 过度阻断而建立的 profile 语义。

## 1.2 release-gate 下已有规则足以阻断

后续 probe 将同类文档按 `controlled + release-gate` 评价，两次均得到：

```text
QUALITY_BAND=FAIL
GATE_DECISION=BLOCK
```

即使排除 HF-9，报告仍指出：

- Actionability 约为 1.0；
- Evidence traceability 约为 1.0–1.5；
- 总分低于 75；
- reader 无法执行复现实验；
- load-bearing result claims 无可运行的支撑链；
- non-compensatory rule 被触发。

因此不存在“没有 HF-REPRO 就无法阻断不可复现实验报告”的证据。

## 1.3 当前 gold 把 release-gate 假设写进了 audit 案例

当前 manifest 同时写了：

```yaml
profile:
  provenance_policy: external
  decision_mode: audit
```

和：

```yaml
expected:
  gate_decision: BLOCK
```

这两个设定在 ADR-DQE-001 的当前语义下不一致。

案例本身可以作为“负质量样例”，但不能继续作为“必须非 ALLOW 的发布负例”。

---

# 2. 语料重构方案

建议将当前案例重构为一个正式 profile pair。

## 2.1 新 pair 命名

建议使用：

```text
BP-006-audit
BP-006-release
```

目录：

```text
tests/corpus/cases/boundary-pairs/BP-006-audit/
tests/corpus/cases/boundary-pairs/BP-006-release/
```

共同字段：

```yaml
pair_id: BP-006
difference_under_test: >
  The same unreproducible experiment-report body is evaluated as
  external+audit versus controlled+release-gate.
```

角色：

```yaml
BP-006-audit:
  class: boundary-pass
  pair_role: pass

BP-006-release:
  class: boundary-fail
  pair_role: fail
```

这样现有 `validate_case_manifests.py` 和 `aggregate_eval_results.py` 可以直接使用 boundary-pair 逻辑。

## 2.2 `BP-006-audit`

来源：当前 `GN-EXP-REPRO-001` 的外部文档版本。

建议 manifest：

```yaml
case_id: BP-006-audit
case_version: 1
class: boundary-pass
pair_id: BP-006
pair_role: pass
artifact_type: experiment-report

profile:
  provenance_policy: external
  decision_mode: audit
  evidence_requirement: key-claims
  reader_test: reproducibility-execution
  output_mode: audit

expected:
  document_quality: PASS
  quality_band: PARTIAL
  gate_decision: ALLOW
  reader_test: FAIL
  required_blockers: []
  forbidden_blockers:
    - HF-9
    - HF-13
    - HF-14a
    - HF-14b
    - HF-15
  required_findings:
    - missing-code-version
    - missing-execution-entry
    - missing-hyperparameters
    - missing-environment
    - missing-reproduction-tolerance
```

这里的 `document_quality: PASS` 只是 `GATE_DECISION=ALLOW` 的兼容映射，不代表整体质量为 PASS。

## 2.3 `BP-006-release`

正文主体与 `BP-006-audit` 保持一致，但增加完整、有效的本地 frontmatter，消除 HF-9 干扰。

建议 frontmatter 至少包含：

```yaml
document_lifecycle: ACCEPTED
generated_by_skill: experiment-provenance-and-reproducibility
skill_version: 0.1.0
source_commit: repro-fixture@<pinned>
source_documents:
  - source-recipe.md
last_verified: 2026-08-02
```

profile：

```yaml
profile:
  provenance_policy: controlled
  decision_mode: release-gate
  evidence_requirement: key-claims
  reader_test: reproducibility-execution
  output_mode: audit
```

预期：

```yaml
expected:
  document_quality: FAIL
  gate_decision: BLOCK
  reader_test: FAIL

  # QUALITY_BAND 由重新双评审确定，不应直接继承 probe。
  quality_band: <PARTIAL-or-FAIL-after-adjudication>

  # 不要求新增专属 HF-REPRO。
  required_blockers: []

  # 必须证明阻断不是由 metadata 或无关结构问题造成。
  forbidden_blockers:
    - HF-9
    - HF-13
    - HF-14a
    - HF-14b
    - HF-15

  required_findings:
    - missing-code-version
    - missing-execution-entry
    - missing-hyperparameters
    - missing-environment
    - missing-reproduction-tolerance
    - reader-cannot-reproduce
```

如果评估器通过 HF-12A/E 形成 BLOCK，可保留这些 blocker；但不建议在 gold 中强制要求固定的 HF-12A/E 组合，因为两个 probe 的 blocker 组合并不完全一致，而最终 gate 与核心 finding 一致。

## 2.4 保留历史

当前案例不应被无痕覆盖。

建议移动到：

```text
tests/corpus/cases/quarantine/GN-EXP-REPRO-001-v1/
```

并添加：

```yaml
reason: profile-expectation-mismatch
superseded_by:
  - BP-006-audit
  - BP-006-release
```

旧诊断结果和原始 manifest 保持可追溯。

---

# 3. 新 pair 的纯度要求

这组测试的目标不是比较 frontmatter，而是比较 profile 下的 gate 语义。因此需要增加下面的确定性约束。

## 3.1 正文主体等价

增加 body-normalized hash：

```yaml
pair_invariants:
  normalized_body_sha256_equal: true
  allowed_differences:
    - local-traceability-frontmatter
    - evaluation-profile
```

`validate_mutation_semantics.py` 应：

1. 去除 YAML/HTML frontmatter；
2. 规范化换行；
3. 比较正文 SHA-256；
4. 若正文不同则报错。

## 3.2 HF-9 不得污染 release 侧

`BP-006-release` 必须先通过：

```text
frontmatter_check.py
status_vocab_check.py
```

再进入模型评测。

如果 release 侧出现 HF-9：

```text
CASE_INVALID
```

而不是将它计为 DQE 正确 BLOCK。

## 3.3 findings 必须出现

两侧都必须识别 reproducibility findings。差异只应体现在：

```text
audit   -> findings + PARTIAL + ALLOW
release -> findings + BLOCK
```

若 audit 侧完全没有识别这些问题，不能因为 gate 为 ALLOW 就算通过。

---

# 4. 必须补强的 harness 项目

## 4.1 准入应以显式 expected gate 为主，而不是仅按 class 推断

当前 `aggregate_eval_results.py` 计算 false pass/fail 时主要使用：

```python
POS = {"golden-positive", "boundary-pass"}
NEG = {"golden-negative", "boundary-fail"}
```

并按 class 判断：

```text
negative + ALLOW     -> false pass
positive + non-ALLOW -> false fail
```

虽然这对普通正负例有效，但无法自然表达：

```text
quality negative / advisory finding / gate ALLOW
```

建议改为：

```text
PRIMARY:
  got_gate == expected.gate_decision

SECONDARY:
  class-based positive/negative metric
```

新的核心指标：

```text
gate_expectation_mismatch_count == 0
```

即：

```python
gate_mismatch = got_gate != exp_gate
```

class 继续用于：

- 语料组织；
- boundary ordering；
- 传统 false-positive/false-negative 统计。

但不应覆盖 manifest 已明确给出的 `expected.gate_decision`。

这能防止未来再次因为“目录名叫 negative”而把合法的 audit ALLOW 算作错误。

## 4.2 required findings 目前未进入自动聚合

manifest 已经大量使用：

```yaml
required_findings:
```

但当前聚合器主要检查：

- gate；
- required blockers；
- forbidden blockers；
- pair ordering；
- stability。

因此一个案例可能因为错误理由得到 BLOCK，却仍被统计为通过。

建议增加 machine-readable 输出：

```text
FINDING_CODES=[missing-code-version,missing-environment,...]
```

并在：

```text
SKILL.md
make_grading_injection.py
score_grading.py
aggregate_eval_results.py
```

中支持：

```text
required_finding_recall
forbidden_finding_violation
```

最低准入标准建议：

```text
required_finding_recall >= 0.90
```

这项改动属于测试可观测性，不改变 DQE 的判别规则。

如果不希望在 v0.4.0 继续修改结构化输出，可先采用独立 meta-grader，但在正式提升为 `provisional-gate` 前，最好将 finding codes 机器化。

## 4.3 修复 diagnostic 中的 stale path

诊断报告指出 `GP-EXP-001` 的 checker 使用了 stale path，导致：

```text
files_checked=0
```

虽然 injection 内嵌文档正确，当前 verdict 仍可参考，但完整 admission 前必须修复。

要求：

- 所有 checker target 必须从 manifest 的 `document` 字段生成；
- 禁止诊断脚本硬编码 case 路径；
- runner 写入：

  ```text
  CHECKER_TARGET=<resolved path>
  CHECKER_FILES_CHECKED=<n>
  ```

- 对单文档 case：

  ```text
  CHECKER_FILES_CHECKED >= 1
  ```

  否则运行记为 harness error，不进入指标。

## 4.4 修复聚合报告的硬编码版本信息

当前 `aggregate_eval_results.py` 生成的标题和正文仍硬编码：

```text
documentation-quality-evaluator v0.3
Corpus dataset_version 3
```

应从以下任一来源读取：

- raw-results metadata；
- eval-plan metadata；
- corpus registry；
- CLI 参数。

建议：

```json
{
  "skill_version": "0.4.0",
  "dataset_version": 4,
  "run_id": "admission-2026-08-xx"
}
```

聚合报告不得再硬编码版本。

---

# 5. 对 v0.4 Skill 更改的评审结论

当前 v0.4 的核心行为可以接受，暂不需要修改判别逻辑。

## 5.1 已得到验证的部分

- profile-aware HF-9 正常；
- external 文档不再因本地 frontmatter 缺失而 BLOCK；
- controlled 文档仍受 HF-9 约束；
- HF-14b 的 release/audit severity map 正常；
- 双轴 verdict 正常；
- profile echo 39/39；
- HF-12A、HF-15 召回稳定；
- HF-13、HF-14a 没有错误触发；
- proposal 缺少发布必要部分时能够稳定给出 non-ALLOW；
- 所有诊断 case 3/3 一致。

## 5.2 不应执行的修改

本轮不要：

- 新增 HF-REPRO；
- 加强 HF-12A；
- 加强 HF-15；
- 修改 HF-13/HF-14a 阈值；
- 将 `external + audit` 的 reproducibility finding 强制升级为 BLOCK；
- 为了让旧 negative 指标变绿而回退 profile-aware HF-9。

## 5.3 建议的小型一致性修复

这些不改变模型判断，但应在 Phase E 前处理。

### A. 更新 Skill description

frontmatter description 仍使用“emit a pass/fail verdict”，建议改为：

```text
emit a two-axis quality-band and gate-decision verdict
```

### B. 更新 Purpose 文案

当前 Purpose 仍主要描述：

```text
DOCUMENT_QUALITY vs FACTUAL_VALIDITY
```

建议同时明确：

```text
QUALITY_BAND vs GATE_DECISION
```

### C. 修正 Workflow step 2 的歧义

当前文字仍称：

```text
HARD checkers ... block
```

但 v0.4 的真实契约是：

```text
checker produces raw finding
evaluator maps severity using profile
```

尤其 HF-9 不应在 checker 层直接宣称 blocker。

### D. 实现或撤回 legacy `status:` deprecation warning

ADR-DQE-001 声称 legacy `status:` 会产生 deprecation warning，但当前 `status_vocab_check.py` 只继续接受旧字段，没有输出 warning。

二选一：

```text
1. 实现 warning；或
2. 修订 ADR，说明 transition 期仅兼容、不警告。
```

建议实现 warning，但 warning 不影响 exit code。

---

# 6. 下一阶段执行顺序

## Phase D.1：解决 OQ-REPRO

1. 在 OQ 报告和 ADR 中写入：

   ```text
   OQ-REPRO=RESOLVED
   decision=A
   HF-REPRO=NOT-ADOPTED
   ```

2. quarantine 当前 `GN-EXP-REPRO-001`；
3. 创建 `BP-006-audit` 和 `BP-006-release`；
4. 增加 normalized-body hash invariant；
5. 确保 release 侧 frontmatter checker 通过。

## Phase D.2：重新审定

Reviewer A/B 继续：

- 不读取 DQE Skill；
- 不读取 hard-fail/rubric；
- 不读取 expected fields；
- 只读取 document、artifact type 和 profile。

但 reviewer contract 应明确中性 profile 语义：

```text
audit:
  gate recommendation is advisory; a quality defect may yield PARTIAL/ALLOW.

release-gate:
  unresolved release-critical defects yield BLOCK or INCOMPLETE.
```

这不是泄露 expected label，而是使 reviewer 正确理解调用场景。

期望：

```text
BP-006-audit:
  gate consensus = ALLOW

BP-006-release:
  gate consensus = BLOCK
```

若 release 侧 reviewer 仍一致 ALLOW，不得人工覆盖；应重新审视“不可复现是否一定阻止该工作流”的产品需求。

## Phase D.3：affected diagnostic rerun

只重跑：

```text
BP-006-audit   × 3
BP-006-release × 3
```

以及 stale-path 修复后的：

```text
GP-EXP-001 × 1 或 ×3
```

通过条件：

```text
BP-006 ordering = 100%
audit findings recall >= 0.90
release findings recall >= 0.90
release forbidden HF-9 violation = 0
all gate decisions stable
checker files_checked >= 1
```

完成后诊断矩阵应从 7/8 提升为 8/8。

---

# 7. Phase E：完整 admission matrix

诊断清零后运行三个 arm：

```text
with_dqe_v0.4
with_dqe_v0.3_frozen
without_skill
```

## 7.1 测试内容

- 全部 live cases；
- 不包含 quarantine；
- 至少 5 个代表案例做 3-run stability；
- profile pairs 全部纳入；
- required findings 自动评分或 meta-grade；
- checker target/read-set 审计。

## 7.2 核心指标

```text
gate_expectation_mismatch_count = 0
golden/boundary negative false ALLOW = 0
golden/boundary positive false non-ALLOW = 0
required_blocker_recall >= 0.90
required_finding_recall >= 0.90
forbidden_blocker_violation_rate = 0
boundary_pair_ordering = 1.0
three_run_gate_consistency = 1.0
max_score_stddev <= 5
profile_echo_compliance = 1.0
checker_execution_compliance = 1.0
```

## 7.3 baseline 增益

DQE v0.4 至少应在以下任一方面显著优于 no-skill：

- profile 条件下的 gate accuracy；
- required finding recall；
- blocker precision；
- repeated-run consistency；
- 不把 external conventions 错当 local blockers；
- 不预测虚假 PASS；
- 结构化输出完整性。

v0.4 也必须优于冻结 v0.3，尤其是：

```text
HF-9 external false BLOCK
HF-14b audit false BLOCK
profile echo
two-axis verdict
```

---

# 8. Promotion 决策

完整 admission 通过后：

```yaml
documentation-quality-evaluator:
  version: 0.4.0
  status: provisional-gate
  disable-model-invocation: true
  auto_trigger: false
  invocation: manual-orchestrator-only
  terminal_gate_authority: limited
```

`limited` 的含义：

- 可作为 Batch 2 文档输出的准入门；
- PASS/ALLOW 仍保留抽查；
- 不自动发布；
- 不自动修改目标；
- 不对普通写作任务自动触发；
- 新 artifact type 在积累足够测试前不自动纳入正式 gate。

随后解锁 Batch 2：

1. `document-information-architect`
2. `research-question-and-literature-planner`
3. `research-evidence-synthesizer`
4. `workspace-forensics-and-inventory`

---

# 9. 给本地 Agent 的执行提示词

```text
请处理 DQE v0.4 的最后一个 OQ-REPRO 问题。

决策已确定：

- 采用 Option A；
- 不新增 HF-REPRO；
- 当前 external+audit 的 GN-EXP-REPRO-001 应为
  QUALITY_BAND=PARTIAL、GATE_DECISION=ALLOW；
- 新增 controlled+release-gate 的 reproducibility BLOCK 案例；
- 现有 DQE 判别逻辑不因本问题修改。

执行步骤：

1. 将 GN-EXP-REPRO-001 v1 移入 quarantine，保留历史结果。
2. 创建 BP-006-audit：
   - external + audit；
   - boundary-pass；
   - expected PARTIAL / ALLOW；
   - 必须报告全部 reproducibility findings；
   - HF-9/HF-13/HF-14a/HF-14b/HF-15 均不得作为 blocker。
3. 创建 BP-006-release：
   - controlled + release-gate；
   - boundary-fail；
   - 增加完整 local traceability frontmatter；
   - 正文与 audit 侧去除 frontmatter 后 SHA-256 相同；
   - expected non-ALLOW，推荐 BLOCK；
   - HF-9 必须 forbidden；
   - 不要求新增 HF-REPRO。
4. 修改 semantic validator，验证 pair 正文等价与 release frontmatter 完整。
5. 更新 reviewer contract，明确 audit 与 release-gate 的中性语义。
6. 重新进行隔离 Reviewer A/B 审定，不得使用 DQE 生成 gold。
7. 修复 diagnostic runner 的 stale checker path；files_checked=0 的 run 视为 harness error。
8. 修改 aggregate_eval_results.py：
   - 以 expected.gate_decision 与实际 gate 的比较作为主要正确性指标；
   - class-based 正负统计保留为次级指标；
   - 删除 v0.3 / dataset v3 硬编码；
   - 从 run metadata 读取版本。
9. 将 required_findings 纳入机器评分：
   - 优先增加 FINDING_CODES=[...]；
   - 计算 required_finding_recall；
   - 防止“因错误原因 BLOCK”被算作通过。
10. 处理 Skill 文案一致性：
    - description 改为 two-axis verdict；
    - Purpose 明确 QUALITY_BAND vs GATE_DECISION；
    - checker raw finding / profile severity 文案一致；
    - 实现或撤回 legacy status deprecation warning。
11. 重跑 BP-006-audit/release 各 3 次及 GP-EXP checker 路径回归。
12. 诊断 8/8 后运行 Phase E：
    - v0.4
    - frozen v0.3
    - without-skill
13. 满足全部 promotion bar 后，将 DQE 提升为 provisional-gate，并解锁 Batch 2。

禁止：

- 新增 HF-REPRO；
- 为 external+audit 强制 BLOCK；
- 修改 HF-12A/HF-15/HF-13/HF-14a 判别阈值；
- 用旧 golden-negative class 覆盖显式 profile 契约；
- 让 checker 未实际读取文件的运行进入准入指标；
- 仅凭 gate 正确而忽略 required findings。
```

---

# 10. 目标终态

```text
OQ-REPRO: RESOLVED
Decision: Option A
HF-REPRO: NOT ADOPTED
BP-006 audit/release pair: adjudicated and stable
Diagnostic: 8/8
Harness stale path: fixed
Gate scoring: expected-gate driven
Required findings: machine-scored
Full admission: completed
DQE: provisional-gate
Batch 2: unlocked
Auto-trigger: still disabled
```

核心原则：

> “不可复现”是明确的质量缺陷；它是否阻止工作流，取决于调用 profile。测试必须同时验证缺陷识别和 profile 下的 gate 行为，而不能用一个 `golden-negative` 标签覆盖两者。
