<!--
generated_by_skill: (manual, Phase E canary decision brief)
skill_version: documentation-quality-evaluator 0.4.1 (candidate; HALTED at Phase E canary)
source_documents:
  - docs/third-party-suggestions/DQE_D3决策与PhaseE安全准入计划.md (Phase E 计划)
  - tests/corpus/blind-runs/phase-e-2026-08-05/canary-summary.md (原始证据)
  - docs/skill-development/reports/dqe-v0.4-defect-ledger.md (D-17)
status: 决策待定 — 需要你在 D-17 的 A/B/C 中裁决后才继续
last_verified: 2026-08-05
-->

# DQE v0.4.1 — Phase E 前置就绪 + Canary 失败汇报与 D-17 决策请求

> **一句话：** Phase E 的全部安全前置项已按计划建成并通过校验；但按计划要求的 **2-slot canary 未通过并已自动
> 停止 Phase E**——`BP-006-release`（受控+发布门）在冻结候选包上**稳定 ALLOW ×3**（金标准=BLOCK）。根因是
> **你此前两条决策 D-16 与 OQ-REPRO=A 在实现层相互冲突**。**我没有改动任何 skill 判定逻辑、没有安装、没有推送。**
> 需要你在下方 **A/B/C** 三个修复方向中裁决后，我才继续。

---

## 0. 你需要做的决策（TL;DR）

`BP-006-release` 是一份**不可复现**的 ResNet-50 实验报告（无超参/训练命令、私有数据"联系作者"、图表与
notebook 断链、"比已发表低 2%"未对账）。两位盲评审都判 **BLOCK**，金标准 gate=BLOCK。但候选 skill v0.4.1
在**同一冻结包、同一输入上跑 3 次，全部 ALLOW**——其中一次甚至在 `QUALITY_BAND=FAIL` + `READER_TEST=FAIL`
的同时输出 `GATE_DECISION=ALLOW`。

请在这三条中选一条（细节见 §5）：

- **A — decision-mode-aware 门路径**：仅在 `release-gate` 下，让"可复现性/执行层失败"驱动 BLOCK；audit 保持
  ALLOW。保住金标准 BLOCK、保住"不加 HF-REPRO"，但**重新把 reader/rubric 耦合进 gate**（须谨慎，且依赖当前
  不稳定的 reader 信号）。
- **B — 采纳 HF-REPRO 硬门**：受控+发布门下，缺 code-version/execution-entry/environment/tolerance 即
  BLOCKER。**最稳健**（基于确定性检测，不靠 LLM 判断），在 D-16 下最干净，但**推翻你的 OQ-REPRO=A /
  HF_REPRO=NOT_ADOPTED 裁决**。
- **C — 缺复现要素 ⇒ INCOMPLETE**：用 D-16 现成的规则 1，把"缺配方/超参/可运行代码"判为缺必需输入 →
  INCOMPLETE（非 ALLOW）。改动最小、完全符合 D-16 与"不加门"，但把该对的 fail 侧金标准从 BLOCK 改判为
  INCOMPLETE。

> **⚠️ 关键前提（§4）**：canary 证明**所有靠 LLM 判断的信号都不稳定**（reader_test 三次 PASS/FAIL/PASS；
> HF-12A 在 D.3 触发、canary 不触发；quality_band PARTIAL/FAIL/PARTIAL）。因此**无论选哪条，稳定修复都需要一个
> "可复现性缺失"的确定性检测器**，否则修完仍会随机翻车。这一点会实质影响 A 的可行性。

---

## 1. Phase E 前置项：已建成并通过校验 ✅

严格按 `DQE_D3决策与PhaseE安全准入计划.md` §2–§6 执行。**全部为测试/工具/治理侧**，skill 判定逻辑字节未变。

| 前置项 | 产物 | 校验 |
|---|---|---|
| 候选版本 0.4.0→**0.4.1** | `SKILL.md`、`skills-registry.yaml`（原**误留 0.3.0**→0.4.1）、两份历史报告加不可变前向横幅、`benchmark-changelog.md`、`last_verified` | 一致 |
| **三个冻结、SHA-256 校验的 bundle** | `evals/skills/snapshots/{dqe-v0.3.0←git 279c0ce, dqe-v0.4.0-pre-d16←git 14959a8, dqe-v0.4.1-candidate←worktree}` + 每个 `SNAPSHOT-MANIFEST.yaml` | v0.3 从 **git 历史**提取（非记忆重建）；hash 校验通过 |
| 注入器增量能力 | `make_grading_injection.py` 增 `--snapshot` 只读注入 + `--role baseline`（无 skill 基线）；**无 `--snapshot` 时行为字节不变** | 冒烟通过 |
| 聚合器 | `aggregate_eval_results.py` 增 `terminal_green`（§3 派生）、`terminal_contract_mismatch_count`、`checker_execution_compliance`、arm 感知 + 对照；单臂向后兼容 | 合成+真实数据测通 |
| manifest | BP-006 对新增 `expected.terminal_green: false`（仅无歧义的两例） | validator 0 error |
| **计划校验器（反失控）** | `scripts/validate_eval_plan.py`：`runs` 为字符串 / 重复 run_key / 超 `MAX_EVAL_RUNS=64` / 快照 hash 不符 / 非 gold 全部 **ABORT_BEFORE_AGENT_CALL** | **对抗测试通过**（string-runs、dup、over-cap 均被拦） |
| 静态计划 | `scripts/make_phase_e_plan.py` → `phase-e-plan.json`：**61 slot**（Arm A v0.4.1 35 = 25 live×1 + 5 稳定×2；Arm B 冻结 v0.3 13；Arm C no-skill 13），预算 ≈5.6M，上限 7.0M | validator 0 error |
| 收尾报告 | `dqe-v0.4.1-diagnostic-close.md` | 已随 canary 结果加更正横幅 |

**这套设计本身按预期生效**：一个 ~0.7M-token 的 canary 探针，拦下了本会在 ~5.6M-token 全矩阵中必然发生的准入
失败，并暴露了一个再多跑矩阵也解决不了的契约冲突。

---

## 2. Canary 结果（§8 硬门）

按计划 §8，正式矩阵前只跑 2 slot；**不通过则 Phase E 自动停止**。我实际跑了 5 slot（release 侧加跑到 3 次以
区分"偶发"与"稳定"）。

| run_key | QUALITY_BAND | GATE_DECISION | READER_TEST | FACTUAL | blockers | files_checked |
|---|---|---|---|---|---|---|
| `v041__BP-006-audit__1` | PARTIAL | **ALLOW** ✅ | PASS | UNVERIFIED | [] | 1 |
| `v041__BP-006-release__1` | PARTIAL | **ALLOW** ❌(金=BLOCK) | PASS | UNVERIFIED | [] | 1 |
| `v041__BP-006-release__2` | **FAIL** | **ALLOW** ❌ | **FAIL** | UNVERIFIED | [] | 1 |
| `v041__BP-006-release__3` | PARTIAL | **ALLOW** ❌ | PASS | UNVERIFIED | [] | 1 |

聚合（候选臂，BP-006 对）：`gate_expectation_mismatch_count=1`、`golden_negative_false_pass=1`、
`boundary_pair_ordering=0.0`、`three_run_verdict_consistency=1.0`（**ALLOW 是稳定的**，非抖动）、
`terminal_contract_mismatch_count=0`（terminal_green 派生正确）、`checker_execution_compliance=1.0`。

- **audit 侧正确**：ALLOW / PARTIAL / `terminal_green=false`（UNVERIFIED）——一个"发现问题但建议放行、且不是绿色
  终端门"的正确形态。
- **release 侧稳定误判**：`run 2` 是铁证——skill 自己判 `QUALITY_BAND=FAIL`、`READER_TEST=FAIL`、列全所有
  不可复现缺陷，**却仍 `GATE_DECISION=ALLOW`**。一份 FAIL 质量、reader 失败、不可复现的文档在发布门下被放行。

---

## 3. 根因：D-16 × OQ-REPRO=A 契约冲突（D-17）

这不是随机误差，而是**你此前两条已接受决策在实现层直接矛盾**：

- **D-16（你 ACCEPT）**：`GATE_DECISION` 只由三规则确定——(1) 缺必需/ profile → INCOMPLETE；(2) 有硬门
  BLOCKER → BLOCK；(3) 否则 ALLOW。并**明确规定 rubric 总分与 FACTUAL_VALIDITY 只决定 QUALITY_BAND，绝不移动
  GATE_DECISION**。（这是为修 audit 三态不稳定而定的。）
- **OQ-REPRO=A（你 ACCEPT，`HF_REPRO=NOT_ADOPTED`）**：不可复现的受控+发布门文档，应**靠 rubric 非补偿规则 +
  reader Layer-2** 判 BLOCK，**不设专属门**（`required_blockers: []`）。

**D-16 恰好切断了 OQ-REPRO=A 依赖的那条路径。** 既然"不可复现"没有对应硬门，而 rubric/reader 又被 D-16 禁止
移动 gate，规则 3 的默认结果就是 **ALLOW**——哪怕 QUALITY_BAND=FAIL。之前 D.3 那次"BLOCK×3"只是评审恰好把复现
缺口映射成了 HF-12A/E（判断题）；在冻结候选包上复跑，它稳定地不触发 → 稳定 ALLOW。

> **这也更正了我数小时前写下的 close-out**：D.3 的"BLOCK×3 / 8/8 / OQ-REPRO 由 skill 确认"是**单样本的过度
> 结论**。盲评审仍然 BLOCK（OQ-REPRO=A 对**人**成立），但**在 D-16 门下对 skill 不成立**。已在 close-out 顶部
> 横幅、ledger **D-17**、benchmark-changelog 中如实更正。

---

## 4. 关键洞察：能用于判门的信号必须是确定性的

canary 顺带证明了一件对**所有**修复方案都重要的事——**当前所有依赖 LLM 判断的信号都不稳定**：

| 信号 | 三次 release 运行 | 稳定？ |
|---|---|---|
| `READER_TEST` | PASS / FAIL / PASS | ❌ |
| `HF-12A/E` 是否触发 | D.3=是 / canary=否 | ❌ |
| `QUALITY_BAND` | PARTIAL / FAIL / PARTIAL | ❌ |
| 确定性 checker（缺 code/超参/断链/私有数据） | 每次都可检出 | ✅ |

**含义**：任何把 gate 押在 reader_test 或"评审是否想起触发 HF-12A"上的修法（尤其是 **A**）都会继承这种抖动，
修完仍会随机翻车。**稳定的修复必须把"不可复现"落到一个确定性检测器上**（一个扫"有无可运行配方/超参/执行入口/
环境/容差、有无私有数据与断链"的 checker）。这正是 **B/C 天然优于 A** 的原因：B/C 把门押在确定性缺失上，A 押在
不稳定的判断上。

---

## 5. 三个修复方向详解

> 三者都建议**先加一个确定性"可复现性缺失"检测器**（§4）；区别在于该信号**路由到哪种非 ALLOW gate**，以及
> **是否动你的既有裁决**。

### 选项 A — decision-mode-aware 的 非补偿→门 路径
- **机制**：把 D-16 规则微调为：`decision_mode=release-gate` 且核心执行问题的 reader Layer-2 判"无法复现/无法
  执行"（或某关键维度非补偿 FAIL）时 → BLOCK；`audit` 保持确定性 ALLOW。
- **优点**：保住金标准 **BLOCK**；保住 **不加 HF-REPRO**；audit 侧（BP-006-audit）不受影响，D-16 修的 audit
  稳定性不回退。
- **缺点/风险**：**重新把 reader/rubric 耦合进 gate**——正是 D-16 为消除三态不稳定而移除的东西；且若押在
  `reader_test` 上，会继承 §4 的不稳定（run 1/3 reader=PASS 仍会 ALLOW）。要可靠，A **实际也得**加 §4 的确定性
  检测器，届时 A ≈「B 的检测器 + BLOCK 路由」。
- **对 gold/指标**：金标准不变（BLOCK）；boundary ordering 恢复 1.0。
- **改动面**：SKILL.md gate 派生规则 + EVALUATOR_CONTRACT + 新 checker + 定向复跑。中等。

### 选项 B — 采纳 HF-REPRO 硬门
- **机制**：新增可复现性硬门：受控+发布门下，缺 {code-version, execution-entry, environment, tolerance}
  （+私有数据/断链）即 **BLOCKER** → 经 D-16 规则 2 → BLOCK。external/audit ⇒ MINOR/N-A（BP-006-audit 保持
  ALLOW）。
- **优点**：**最稳健**——门押在确定性检测上；在 D-16 下**最干净**（硬门 → BLOCK，无需动 gate 派生规则）；
  精确匹配金标准 BLOCK 与两位盲评审。
- **缺点/风险**：**推翻你 OQ-REPRO=A / `HF_REPRO=NOT_ADOPTED`（你已两次坚持不加）**；增加 skill 硬门表面积；
  需要一张 HF-REPRO 的 profile-severity 表（类似 HF-14b）。
- **对 gold/指标**：金标准不变（BLOCK）；`required_blockers` 从 `[]` 变为 `[HF-REPRO]`；ordering 恢复 1.0。
- **改动面**：hard-fail.md 新门 + checker + SKILL/contract + ADR 更新 + 定向复跑。中—大。

### 选项 C — 缺复现要素 ⇒ INCOMPLETE（用 D-16 现成规则 1）
- **机制**：把"发布门下缺可运行配方/超参/执行入口"判为**缺必需输入** → 经 D-16 **规则 1** → **INCOMPLETE**
  （非 ALLOW）。配合 §4 的确定性检测器来稳定触发。
- **优点**：**完全符合 D-16**（用现成规则 1，不让 rubric/reader 移动 gate）；**不加硬门**（尊重
  HF_REPRO=NOT_ADOPTED）；改动最小；产出正确的非 ALLOW；语义上"缺复现必需内容 = 尚不能批准"其实比"有缺陷要修
  = BLOCK"更贴切。
- **缺点/风险**：把该对 fail 侧金标准从 **BLOCK 改判 INCOMPLETE**（两位盲评审说 BLOCK）；"INCOMPLETE vs BLOCK"
  的语义边界需在 ADR 里说清（present-defect vs missing-input）。
- **对 gold/指标**：BP-006-release 金标准 gate 改为 INCOMPLETE；boundary ordering 仍成立（pass=ALLOW /
  fail∈{BLOCK,INCOMPLETE}）；ordering 恢复 1.0。
- **改动面**：SKILL/contract 一处澄清 + checker + manifest 金标准改判 + ADR 记录 + 定向复跑。**最小**。

### 对比速览

| 维度 | A | B | C |
|---|---|---|---|
| 保住金标准 BLOCK | ✅ | ✅ | ❌（改 INCOMPLETE） |
| 尊重"不加 HF-REPRO" | ✅ | ❌（推翻） | ✅ |
| 完全符合 D-16 决定论 | ❌（重新耦合） | ✅ | ✅ |
| 稳健性（不靠 LLM 判断） | ⚠️（须补检测器） | ✅ 最强 | ✅ |
| 改动面 | 中 | 中—大 | 最小 |

---

## 6. 我的建议

**首选 C，次选 B；不建议单用 A。** 理由：

1. **§4 决定一切**：稳定修复必须把"不可复现"落到确定性检测，而不是 reader_test/rubric 这些已被证明抖动的
   LLM 判断。这直接淘汰"单用 A"。
2. **C 同时满足最多约束**：完全符合 D-16（不重新耦合、用现成规则 1）+ 尊重你的"不加 HF-REPRO"+ 改动最小 +
   产出稳定的非 ALLOW。代价仅是把 fail 侧金标准改判 INCOMPLETE，而"缺复现必需内容 ⇒ 尚不能批准"在语义上是站得
   住的（两种都正确拒绝放行）。
3. **若你更看重"精确匹配盲评审的 BLOCK + 最强稳健性"**，则选 **B**——它是 D-16 下最干净的形态，只是要你松动
   `HF_REPRO=NOT_ADOPTED`。canary 这份 3/3 稳定误判，正是当初该裁决可以被重新审视的新证据。
4. **A 仅在你坚持"既保 BLOCK 又不加门"时才选**，且必须补 §4 检测器（否则不稳）——那样它本质是"B 的检测器 +
   BLOCK 路由"，复杂度不低于 B。

---

## 7. 未改动 / 安全声明

- **skill 判定逻辑字节未变**：`hard-fail.md`、`rubric.md`、`canonical-source-map.md`、`checkers/**` 本次
  **零改动**；`SKILL.md` 的改动仅为版本号 0.4.1 + D-16 摘要横幅（D-16 门规则文本此前已在 HEAD）。
- **没有实施任何 D-17 修复**（未加门、未改 gate 规则、未改判 gold）。等你裁决。
- **没有安装、没有推送、没有实时加载、没有自动触发**。skill 仍 `disable-model-invocation: true` /
  `experimental`；升 `provisional-gate` 仍被 Phase E 准入门卡住（未通过）。
- **63M-token 失控**已归档为 `HARNESS_ORCHESTRATION_FAILURE`，本轮无背景 Workflow、无循环、无失控面。

## 8. 你裁决后我的下一步（按选项）

- **选 C**：加"可复现性缺失"checker（确定性）→ SKILL/EVALUATOR_CONTRACT 增一条"release-gate + 缺复现必需要素
  ⇒ INCOMPLETE"澄清 → BP-006-release 金标准改 INCOMPLETE（记 ADR）→ 用 §9.3 定向诊断复跑 BP-006 对 ×3 稳定 →
  再校验 `phase-e-plan.json` → 重跑 canary → 通过后按 4-slot 直连批次跑 61-slot 矩阵。
- **选 B**：hard-fail.md 增 HF-REPRO + profile-severity 表 → checker → 更新 ADR（`HF_REPRO` 由 REJECTED 改为
  ADOPTED，附 canary 证据）→ 定向复跑 → 重跑 canary → 矩阵。
- **选 A**：SKILL gate 派生增 decision-mode-aware 分支 + 补 §4 检测器 → 定向复跑验证不回退 audit 稳定性 →
  重跑 canary → 矩阵。
- **任一路径都不再用背景 Workflow**；矩阵启动前会再次打印 exact N / 各臂 slot / 总数 / 预算，并先过
  `validate_eval_plan.py`。

## 附录：本轮产物

- 计划输入：`docs/third-party-suggestions/DQE_D3决策与PhaseE安全准入计划.md`
- canary 证据：`tests/corpus/blind-runs/phase-e-2026-08-05/{canary-summary.md, canary-raw.json, canary-metrics/, results/*.json, injections/}`
- 静态计划：`tests/corpus/blind-runs/phase-e-2026-08-05/phase-e-plan.json`（61 slot，已校验）
- 冻结包：`evals/skills/snapshots/{dqe-v0.3.0, dqe-v0.4.0-pre-d16, dqe-v0.4.1-candidate}/`（含 SNAPSHOT-MANIFEST + SHA-256）
- 新脚本：`scripts/{build_skill_snapshots, make_phase_e_plan, validate_eval_plan}.py`
- 缺陷账本：`docs/skill-development/reports/dqe-v0.4-defect-ledger.md` **D-17**
- 更正的收尾报告：`docs/skill-development/reports/dqe-v0.4.1-diagnostic-close.md`（顶部横幅）
